import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai_mcp import MCPServer, Context
from db import get_db_session
from models import Cliente
from dotenv import load_dotenv

load_dotenv()  # loads .env if present

app = FastAPI(title="indisa_mcp_server - Azure SQL (MCP)")
mcp = MCPServer(name="indisa_mcp_server", version="1.0")

# Simple Pydantic model for HTTP REST endpoint payload/responses
class ClienteOut(BaseModel):
    id: int
    nome: str
    cidade: str | None = None
    email: str | None = None

def cliente_to_dict(cliente: Cliente) -> dict:
    return {
        "id": cliente.id,
        "nome": cliente.nome,
        "cidade": cliente.cidade,
        "email": cliente.email,
    }

# MCP tool: get_cliente
@mcp.tool(
    name="get_cliente",
    description="Recupera informações de um cliente pelo ID no banco de dados Azure SQL. Retorna campos id, nome, cidade e email."
)
def get_cliente(context: Context, id: int):
    """MCP-exposed function. The LLM can call this directly via MCP client/sdk."""
    with get_db_session() as session:
        cliente = session.query(Cliente).filter(Cliente.id == id).one_or_none()
        if not cliente:
            return {"error": "cliente_nao_encontrado", "id": id}
        return cliente_to_dict(cliente)

# Optional: expose a REST endpoint for direct HTTP use / debugging
@app.get("/clientes/{id}", response_model=ClienteOut)
def get_cliente_http(id: int):
    with get_db_session() as session:
        cliente = session.query(Cliente).filter(Cliente.id == id).one_or_none()
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        return cliente_to_dict(cliente)

# Register MCP tools into FastAPI so MCP server endpoints are exposed
mcp.register_api(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True)
