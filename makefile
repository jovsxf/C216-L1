BACKEND_DIR=backend
POETRY=py -3.11 -m poetry
DOCKER_COMPOSE=docker compose

# Stack isolada para os testes E2E: projeto, portas e volume próprios.
E2E_PROJECT=lab-e2e
E2E_COMPOSE=$(DOCKER_COMPOSE) -p $(E2E_PROJECT)
E2E_FRONTEND_PORT=5174
E2E_API_PORT=8001
E2E_DB_PORT=5434

.PHONY: help install run test lint format check db-upgrade db-current db-migration db-upgrade-local up up-build down ps logs restart e2e frontend-install frontend-dev frontend-lint frontend-format frontend-check frontend-test frontend-test-e2e frontend-build check-all

help:
	@echo "Comandos disponiveis:"
	@echo "  make install          - Instala as dependencias do backend"
	@echo "  make run              - Executa a API localmente (sem Docker)"
	@echo "  make test             - Executa os testes do backend com Pytest"
	@echo "  make lint             - Verifica o estilo do codigo com Ruff"
	@echo "  make format           - Formata o codigo com Ruff"
	@echo "  make check            - Verifica a configuracao do Poetry"
	@echo "  make up-build         - Constroi e sobe db, api e frontend"
	@echo "  make up               - Sobe db, api e frontend"
	@echo "  make down             - Para e remove os containers"
	@echo "  make ps               - Mostra o estado dos containers"
	@echo "  make logs             - Exibe os logs dos containers"
	@echo "  make restart          - Reconstroi e reinicia os containers"
	@echo "  make db-upgrade       - Aplica as migrations no container da API"
	@echo "  make db-current       - Mostra a revisao atual do banco"
	@echo "  make db-migration     - Gera uma migration (msg=\"descricao\")"
	@echo "  make db-upgrade-local - Aplica as migrations sem Docker"
	@echo "  make frontend-install - Instala dependencias do frontend"
	@echo "  make frontend-dev     - Executa o frontend localmente"
	@echo "  make frontend-check   - Verifica lint e formatacao (Biome)"
	@echo "  make frontend-test    - Executa testes Vitest"
	@echo "  make frontend-test-e2e - Executa Playwright contra a stack no ar"
	@echo "  make frontend-build   - Gera build de producao"
	@echo "  make e2e              - E2E full-stack em stack isolada ($(E2E_PROJECT))"
	@echo "  make check-all        - Verifica backend e frontend (exige Docker)"

install:
	cd $(BACKEND_DIR) && $(POETRY) install --no-root

run:
	cd $(BACKEND_DIR) && $(POETRY) run uvicorn app.main:app --reload

test:
	cd $(BACKEND_DIR) && $(POETRY) run pytest

lint:
	cd $(BACKEND_DIR) && $(POETRY) run ruff check .

format:
	cd $(BACKEND_DIR) && $(POETRY) run ruff format .

check:
	cd $(BACKEND_DIR) && $(POETRY) check

# --- Docker Compose (db + api + frontend) ---

up:
	$(DOCKER_COMPOSE) up -d

up-build:
	$(DOCKER_COMPOSE) up -d --build

down:
	$(DOCKER_COMPOSE) down

ps:
	$(DOCKER_COMPOSE) ps

logs:
	$(DOCKER_COMPOSE) logs -f

restart:
	$(DOCKER_COMPOSE) down
	$(DOCKER_COMPOSE) up -d --build

db-upgrade:
	$(DOCKER_COMPOSE) exec -T api alembic upgrade head

db-current:
	$(DOCKER_COMPOSE) exec -T api alembic current

db-migration:
	$(DOCKER_COMPOSE) exec -T api alembic revision --autogenerate -m "$(msg)"

db-upgrade-local:
	cd $(BACKEND_DIR) && $(POETRY) run alembic upgrade head

# --- E2E full-stack isolado ---
# Sobe a stack "lab-e2e", aplica as migrations, roda o Playwright e sempre
# derruba tudo com "down -v" (o banco de desenvolvimento nunca e tocado).

e2e: export FRONTEND_PORT=$(E2E_FRONTEND_PORT)
e2e: export API_PORT=$(E2E_API_PORT)
e2e: export DB_PORT=$(E2E_DB_PORT)
e2e: export CORS_ORIGINS=http://localhost:$(E2E_FRONTEND_PORT),http://127.0.0.1:$(E2E_FRONTEND_PORT)
e2e: export VITE_API_URL=http://localhost:$(E2E_API_PORT)
e2e: export E2E_BASE_URL=http://localhost:$(E2E_FRONTEND_PORT)
e2e:
	$(E2E_COMPOSE) up -d --build --wait && \
	$(E2E_COMPOSE) exec -T api alembic upgrade head && \
	npm --prefix frontend run test:e2e; \
	status=$$?; \
	$(E2E_COMPOSE) down -v; \
	exit $$status

# --- Frontend ---

frontend-install:
	npm --prefix frontend ci

frontend-dev:
	npm --prefix frontend run dev

frontend-lint:
	npm --prefix frontend run lint

frontend-format:
	npm --prefix frontend run format

frontend-check:
	npm --prefix frontend run check
	npm --prefix frontend run format:check

frontend-test:
	npm --prefix frontend run test

frontend-test-e2e:
	npm --prefix frontend run test:e2e

frontend-build:
	npm --prefix frontend run build

check-all: lint test frontend-check frontend-test frontend-build e2e
