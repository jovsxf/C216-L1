# C216-L1

Backend de exemplo com FastAPI e frontend React independente para gerenciamento de itens.

## Organização

O código da aplicação fica em `backend/`:

- `app/main.py`: inicializa o FastAPI e registra os routers.
- `app/api/routes/`: endpoints HTTP para itens e informações do sistema.
- `app/schemas/`: modelos Pydantic de entrada e saída.
- `app/services/`: regras de gerenciamento dos itens.
- `app/repositories/`: consultas e gravações via SQLAlchemy.
- `app/models/`: modelos ORM usados para persistência.
- `app/database/`: engine, sessões e dependência de banco da API.
- `alembic/`: migrations versionadas do banco.
- `tests/unit/`: testes unitários dos serviços e funções isoladas.
- `tests/integration/`: testes dos endpoints usando o `TestClient` do FastAPI.

Os endpoints de itens usam `item_id` como parâmetro de caminho (`Path Parameter`). A API oferece GET, POST, PUT, PATCH e DELETE em `/items`.

## Executar a aplicação

Dentro de `backend`, execute:

```bash
poetry run uvicorn app.main:app --reload
```

Por padrão, a execução local usa SQLite em `backend/items.db`. Para usar PostgreSQL, configure `DATABASE_URL` (consulte `.env.example`) ou execute a stack via `docker compose up --build`. No Compose, a API aplica as migrations antes de iniciar.

Use `make db-upgrade` para aplicar migrations localmente, `make db-migration msg="descricao"` para gerar uma revisão e `make lint` para verificar o estilo.

## Executar os testes

Dentro de `backend`, execute:

```bash
poetry run pytest
```

O workflow em `.github/workflows/` instala as dependências e executa toda a suíte em cada push e pull request.

## Frontend (Prática 6)

O frontend em `frontend/` usa React, Vite e Tailwind CSS. Nesta prática, os itens ficam somente em memória no navegador, sem chamadas ao backend.

```bash
make frontend-install
make frontend-dev
```

Para validar o frontend, execute `make frontend-check`, `make frontend-test`, `make frontend-build` e `make frontend-test-e2e`. Na primeira execução E2E, instale o navegador com `npx --prefix frontend playwright install chromium`.
