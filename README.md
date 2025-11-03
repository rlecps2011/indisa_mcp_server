# indisa_mcp_server (Azure SQL - Complete)

Projeto exemplo de um servidor MCP (Model Context Protocol) integrado com Azure SQL.

## Estrutura
- `main.py` - FastAPI app + registro de ferramentas MCP
- `db.py` - criação de engine SQLAlchemy / sessão
- `models.py` - modelo `Cliente` (SQLAlchemy ORM)
- `test_client.py` - scripts simples de teste (REST + MCPClient)
- `requirements.txt` - dependências
- `.env.example` - exemplo de variáveis de ambiente

## Como usar (desenvolvimento)

1. Copie `.env.example` para `.env` e ajuste:
    - `DB_USER`, `DB_PASSWORD`, `DB_SERVER`, `DB_NAME`
    - OU, para testes locais, defina `SQLITE_URL=sqlite:////tmp/test.db`

2. Instale dependências (recomendado em virtualenv):
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

3. (Opcional) Se quiser criar a tabela e inserir um cliente de teste usando SQLite:
    ```python
    # run in python REPL
    from db import engine, SQLITE_URL
    from models import create_tables, Cliente
    create_tables(engine)
    ```

4. Rodar o servidor:
    ```bash
    uvicorn main:app --reload
    ```

5. Testar:
    ```bash
    python test_client.py
    ```

## Observações
- Substitua `openai-mcp` pelo pacote MCP/SDK que você esteja usando caso o nome do pacote seja diferente.
- Em produção no Azure, proteja suas credenciais com Key Vault, Managed Identity ou variáveis de ambiente seguras.

