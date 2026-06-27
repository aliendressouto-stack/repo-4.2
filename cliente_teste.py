# cliente_teste.py
import asyncio
import json
import logging
import os
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Garante que só o envelope JSON vá para o stdout: silencia logs e descarta
# o stderr do processo do servidor MCP.
logging.disable(logging.INFO)


def _extrai(resultado, como_lista=False):
    """Extrai o payload JSON do resultado de um call_tool, tolerando
    variações entre versões do SDK do MCP.

    como_lista=True garante que o retorno seja uma lista. Em algumas versões
    do SDK uma tool que devolve lista vira *um bloco de texto por item*;
    em outras vem tudo em structuredContent.
    """
    # SDKs recentes expõem structuredContent já desserializado.
    structured = getattr(resultado, "structuredContent", None)
    if structured is not None:
        # FastMCP embrulha retornos não-dict (ex.: list) em {"result": ...}.
        if isinstance(structured, dict) and "result" in structured:
            return structured["result"]
        return structured

    # Fallback: desserializa os blocos de texto.
    itens = [json.loads(bloco.text) for bloco in resultado.content]
    if como_lista:
        # Cada bloco já pode ser um item, ou um único bloco pode conter a lista.
        if len(itens) == 1 and isinstance(itens[0], list):
            return itens[0]
        return itens
    return itens[0]


async def main() -> dict:
    params = StdioServerParameters(command=sys.executable, args=["servidor_mcp.py"])
    devnull = open(os.devnull, "w")
    async with stdio_client(params, errlog=devnull) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            nomes = [t.name for t in tools.tools]

            criar = await session.call_tool("criar_tarefa", {"titulo": "tarefa via mcp"})
            listar = await session.call_tool("listar_tarefas", {})

            return {
                "tools": nomes,
                "criar_resultado": _extrai(criar),
                "listar_resultado": _extrai(listar, como_lista=True),
            }


if __name__ == "__main__":
    print(json.dumps(asyncio.run(main())))
