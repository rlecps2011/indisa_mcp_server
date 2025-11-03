from fastapi import FastAPI
from openai_mcp import MCPServer, Context

# Cria app FastAPI + servidor MCP
app = FastAPI(title="indisa_mcp_server - Minimal")
mcp = MCPServer(name="indisa_mcp_server", version="1.0")

# --- Ferramenta MCP simples ---
@mcp.tool(
    name="get_mensagem",
    description="Retorna uma mensagem simples para teste do protocolo MCP."
)
def get_mensagem(context: Context):
    return {"mensagem": "Olá! Este servidor MCP está funcionando 🚀"}

# --- Endpoint HTTP opcional (para debug manual) ---
@app.get("/")
def root():
    return {"status": "ok", "mensagem": "Servidor MCP ativo"}

# Integra FastAPI e MCP
mcp.register_api(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)