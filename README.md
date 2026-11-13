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

Por padrão, a execução local usa SQLite em `backend/items.db`. Para usar PostgreSQL, configure `DATABASE_URL` (consulte `.env.example`) ou execute a stack completa com Docker Compose (veja abaixo).

Use `make db-upgrade-local` para aplicar migrations sem Docker, `make db-migration msg="descricao"` para gerar uma revisão e `make lint` para verificar o estilo.

## Executar os testes

Dentro de `backend`, execute:

```bash
poetry run pytest
```

O workflow em `.github/workflows/` instala as dependências e executa toda a suíte em cada push e pull request.

## Stack full-stack (Prática 7)

O frontend React consome a API FastAPI, que persiste os itens no PostgreSQL.

```text
Navegador (React/Vite) :5173  --fetch + CORS-->  API FastAPI :8000  --SQLAlchemy-->  PostgreSQL (db:5432)
```

- `frontend/src/services/items.js` concentra as chamadas `GET /items/` e `POST /items/` (URL em `VITE_API_URL`).
- A API autoriza apenas as origens listadas em `CORS_ORIGINS` (`backend/app/core/config.py`).
- Nomes duplicados retornam `409` com `{"detail": "Já existe um item com esse nome"}`; nomes vazios ou com mais de 100 caracteres retornam `422`.

### Subir com Docker Compose

```bash
cp .env.example .env   # primeira vez
make up-build          # db + api + frontend
make db-upgrade        # aplica as migrations (Alembic)
make ps                # todos devem ficar "healthy"
```

- Frontend: <http://localhost:5173>
- API / Swagger: <http://localhost:8000/docs>

O código é copiado para as imagens: após alterar o código, rode `make up-build` novamente.

### Testes

| Comando | O que executa |
| --- | --- |
| `make test` | Pytest do backend (SQLite em memória) |
| `make frontend-test` | Vitest: unitários e integração com `fetch` mockado |
| `make frontend-check` / `make frontend-build` | Biome / build do Vite |
| `make e2e` | Playwright contra uma stack isolada (`lab-e2e`, portas 5174/8001/5434), removida ao final com `down -v` |
| `make frontend-test-e2e` | Playwright contra a stack já no ar (`E2E_BASE_URL`, padrão `http://localhost:5173`) |
| `make check-all` | Tudo acima (exige Docker) |

Na primeira execução E2E, instale o navegador com `npx --prefix frontend playwright install chromium`.
