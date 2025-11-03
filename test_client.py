"""Script de teste:
- Testa o endpoint REST /clientes/{id} via HTTP
- Testa a ferramenta MCP via MCPClient (assumes openai_mcp.MCPClient available)
"""
import os
import requests

# Configure URL do servidor
BASE_URL = os.getenv("MCP_BASE_URL", "http://127.0.0.1:8000")

def test_rest(id=1):
    url = f"{BASE_URL}/clientes/{id}"
    print("GET", url)
    resp = requests.get(url, timeout=5)
    print("status:", resp.status_code)
    print(resp.text)

def test_mcp_client(id=1):
    try:
        from openai_mcp import MCPClient
    except Exception as e:
        print("MCPClient import failed:", e)
        return
    client = MCPClient(base_url=BASE_URL)
    result = client.get_cliente(id=id)
    print("MCP get_cliente result:", result)

if __name__ == "__main__":
    print("=== Testando REST ===")
    test_rest(1)
    print("=== Testando MCPClient ===")
    test_mcp_client(1)
