from fastapi import FastAPI

app = FastAPI(title="indisa_mcp_server - 2 tools")


# --- Helper decorator para MCP tools ---
def mcp_tool(path, description):
    def decorator(func):
        app.get(path)(func)  # registra rota FastAPI
        func.context = description  # opcional: mantém contexto
        return func
    return decorator

# --- Tool 1 - ---
@mcp_tool("/get_mensagem", "Retorna mensagem simples para teste da IA")
def get_mensagem():
    return {"mensagem": "Olá! Esta é a primeira tool 🚀"}

# --- Tool 2 ---
@mcp_tool("/get_status", "Retorna status do servidor para a IA")
def get_status():
    return {"status": "Servidor ativo", "uptime": "24h"}  # exemplo fixo

# --- Endpoint raiz opcional ---
@app.get("/")
async def root():
    return {
        "tools": [
            {"name": "get_mensagem", "description": "Retorna mensagem simples para teste da IA", "endpoint": "/get_mensagem"},
            {"name": "get_status", "description": "Retorna status do servidor para a IA", "endpoint": "/get_status"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)