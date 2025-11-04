from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import json
import asyncio
from mcp.server.fastmcp import FastMCP

app = FastAPI(title="indisa_mcp_server - 2 tools")
mcp = FastMCP("Demo")

# --- Helper decorator para MCP tools ---
def mcp_tool(path, description):
    def decorator(func):
        app.get(path)(func)  # registra rota FastAPI
        func.context = description  # opcional: mantém contexto
        return func
    return decorator

# --- Tool 1 - ---

@mcp.tool()
def get_mensagem():
    """Mensagem de Boas Vindas"""
    return {"mensagem": "Olá! Esta é a primeira tool 🚀"}

# --- Tool 2 ---
@mcp.tool()
def get_status():
    """Retorna status do servidor para a IA"""
    return {"status": "Servidor ativo", "uptime": "24h"}  # exemplo fixo

@app.get("/sse")
async def sse_endpoint():
    async def event_generator():
        # Mensagem inicial do MCP
        data = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "indisa-api",
                    "version": "1.0.0"
                }
            }
        }
        yield f"event: message\ndata: {json.dumps(data)}\n\n"
        
        # Manter conexão aberta
        while True:
            await asyncio.sleep(30)
            yield f": keepalive\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }





# --- Endpoint raiz opcional ---
@app.get("/")
async def root():
    return {"message": "Bem-vindo ao indisa_mcp_server!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)