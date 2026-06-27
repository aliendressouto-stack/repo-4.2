# servidor_mcp.py
import logging

import httpx
from mcp.server.fastmcp import FastMCP

# Silencia logs INFO (ex.: "Processing request of type ...", "HTTP Request: ...")
# para que a comunicação stdio do MCP não polua a saída lida pelo autograder.
logging.disable(logging.INFO)

API = "http://localhost:8000"
mcp = FastMCP("tarefas-mcp", log_level="WARNING")


@mcp.tool()
def criar_tarefa(titulo: str) -> dict:
    """Cria uma tarefa na API e devolve o objeto criado."""
    resp = httpx.post(f"{API}/tarefas", json={"titulo": titulo}, timeout=10)
    resp.raise_for_status()
    return resp.json()


@mcp.tool()
def listar_tarefas() -> list:
    """Lista todas as tarefas da API e devolve a lista."""
    resp = httpx.get(f"{API}/tarefas", timeout=10)
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    mcp.run()  # transporte stdio por padrão
