# C216-L1

Backend de exemplo com FastAPI para gerenciamento de itens.

## Organização

O código da aplicação fica em `backend/`:

- `main.py`: inicializa o FastAPI e registra os routers.
- `routes/`: endpoints HTTP para itens e informações do sistema.
- `schemas/`: modelos Pydantic de entrada e saída.
- `services/`: regras de gerenciamento dos itens.
- `tests/unit/`: testes unitários dos serviços e funções isoladas.
- `tests/integration/`: testes dos endpoints usando o `TestClient` do FastAPI.

Os endpoints de itens usam `item_id` como parâmetro de caminho (`Path Parameter`). A API oferece GET, POST, PUT, PATCH e DELETE em `/items`.

## Executar a aplicação

Dentro de `backend`, execute:

```bash
poetry run uvicorn main:app --reload
```

## Executar os testes

Dentro de `backend`, execute:

```bash
poetry run pytest
```

O workflow em `.github/workflows/` instala as dependências e executa toda a suíte em cada push e pull request.
