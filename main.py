from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from mcp.server.fastmcp import FastMCP
import json
import asyncio

# Criar instância do FastMCP
mcp = FastMCP("indisa-api")

# --- Tool 1 ---
@mcp.tool()
def get_mensagem() -> str:
    """Mensagem de Boas Vindas"""
    return "Olá! Esta é a primeira tool 🚀"

# --- Tool 2 ---
@mcp.tool()
def get_status() -> dict:
    """Retorna status do servidor para a IA"""
    return {"status": "Servidor ativo", "uptime": "24h"}

# Criar app FastAPI
app = FastAPI(title="indisa_mcp_server")

@app.get("/sse")
async def handle_sse(request: Request):
    """Endpoint SSE para comunicação MCP"""
    
    async def event_generator():
        try:
            # Mensagem de inicialização
            init_response = {
                "jsonrpc": "2.0",
                "id": 1,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "indisa-api",
                        "version": "1.0.0"
                    }
                }
            }
            
            yield f"data: {json.dumps(init_response)}\n\n"
            
            # Listar tools disponíveis
            tools_list = {
                "jsonrpc": "2.0",
                "method": "notifications/tools/list_changed",
                "params": {
                    "tools": [
                        {
                            "name": "get_mensagem",
                            "description": "Mensagem de Boas Vindas",
                            "inputSchema": {
                                "type": "object",
                                "properties": {},
                                "required": []
                            }
                        },
                        {
                            "name": "get_status",
                            "description": "Retorna status do servidor para a IA",
                            "inputSchema": {
                                "type": "object",
                                "properties": {},
                                "required": []
                            }
                        }
                    ]
                }
            }
            
            yield f"data: {json.dumps(tools_list)}\n\n"
            
            # Manter conexão aberta com keepalive
            while True:
                if await request.is_disconnected():
                    break
                await asyncio.sleep(30)
                yield ": keepalive\n\n"
                
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"Erro no SSE: {e}")
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@app.post("/message")
async def handle_message(request: Request):
    """Endpoint para receber chamadas de tools"""
    try:
        body = await request.json()
        method = body.get("method")
        params = body.get("params", {})
        msg_id = body.get("id")
        
        # Chamar tool apropriada
        if method == "tools/call":
            tool_name = params.get("name")
            
            if tool_name == "get_mensagem":
                result = get_mensagem()
            elif tool_name == "get_status":
                result = get_status()
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {
                        "code": -32601,
                        "message": f"Tool não encontrada: {tool_name}"
                    }
                }
            
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result) if isinstance(result, dict) else str(result)
                        }
                    ]
                }
            }
        
        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "tools": [
                        {
                            "name": "get_mensagem",
                            "description": "Mensagem de Boas Vindas",
                            "inputSchema": {
                                "type": "object",
                                "properties": {},
                                "required": []
                            }
                        },
                        {
                            "name": "get_status",
                            "description": "Retorna status do servidor para a IA",
                            "inputSchema": {
                                "type": "object",
                                "properties": {},
                                "required": []
                            }
                        }
                    ]
                }
            }
        
        return {"jsonrpc": "2.0", "id": msg_id, "result": {}}
        
    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "id": body.get("id") if body else None,
            "error": {
                "code": -32603,
                "message": str(e)
            }
        }

@app.get("/")
async def root():
    return {
        "message": "Bem-vindo ao indisa_mcp_server!",
        "tools": ["get_mensagem", "get_status"],
        "endpoints": {
            "sse": "/sse",
            "message": "/message"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)