# Exercício 4.2 — MCP server local que consome a API do 4.1

Este repositório implementa um **MCP server** (Model Context Protocol) que fica
na frente da API REST de TODO list construída no Exercício 4.1. O MCP é a camada
do meio que traduz pedidos de um agente/LLM em chamadas HTTP para a API.

```
Agente / LLM   ──MCP──▶   servidor_mcp.py   ──HTTP──▶   API 4.1 (localhost:8000)
```

## Arquivos

| Arquivo | Descrição |
|---|---|
| `servidor_mcp.py` | MCP server (stdio) que expõe duas tools que chamam a API 4.1 |
| `cliente_teste.py` | Sobe o server, exercita as tools e imprime o envelope JSON |
| `requirements.txt` | Dependências (`mcp`, `httpx`) |

## Tools expostas

| Tool | Assinatura | O que faz |
|---|---|---|
| `criar_tarefa` | `criar_tarefa(titulo: str) -> dict` | `POST /tarefas` e devolve a tarefa criada |
| `listar_tarefas` | `listar_tarefas() -> list` | `GET /tarefas` e devolve a lista |

## Como rodar localmente

**Terminal A** — suba a API do 4.1 (reinicie para o store ficar limpo):

```bash
uvicorn app.main:app --port 8000     # no repo do 4.1
```

**Terminal B** — no repo do 4.2:

```bash
pip install -r requirements.txt
python cliente_teste.py
```

Deve imprimir o envelope JSON com `tools`, `criar_resultado` e `listar_resultado`.

## Validação

Com a API do 4.1 no ar:

```bash
autograde validar 4.2
```
