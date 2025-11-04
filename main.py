from fastapi import FastAPI
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

# --- Endpoint raiz opcional ---
@app.get("/")
async def root():
    return {"message": "Bem-vindo ao indisa_mcp_server!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)