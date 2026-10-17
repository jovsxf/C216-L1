BACKEND_DIR=backend
POETRY=py -3.11 -m poetry
DOCKER_COMPOSE=docker compose

.PHONY: help install run test lint format check db-upgrade db-current db-migration docker-build docker-up docker-down docker-logs docker-restart

help:
	@echo "Comandos disponiveis:"
	@echo "  make install        - Instala as dependencias"
	@echo "  make run            - Executa a aplicacao localmente"
	@echo "  make test           - Executa os testes automatizados com Pytest"
	@echo "  make lint           - Verifica o estilo do codigo com Ruff"
	@echo "  make format         - Formata o codigo com Ruff"
	@echo "  make db-upgrade     - Aplica as migrations"
	@echo "  make db-current     - Mostra a revisao atual do banco"
	@echo "  make check          - Verifica a configuracao do Poetry"
	@echo "  make docker-build   - Constroi as imagens Docker"
	@echo "  make docker-up      - Inicia os containers"
	@echo "  make docker-down    - Para e remove os containers"
	@echo "  make docker-logs    - Exibe os logs dos containers"
	@echo "  make docker-restart - Reinicia os containers"

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

db-upgrade:
	cd $(BACKEND_DIR) && $(POETRY) run alembic upgrade head

db-current:
	cd $(BACKEND_DIR) && $(POETRY) run alembic current

db-migration:
	cd $(BACKEND_DIR) && $(POETRY) run alembic revision --autogenerate -m "$(msg)"

check:
	cd $(BACKEND_DIR) && $(POETRY) check

docker-build:
	$(DOCKER_COMPOSE) build

docker-up:
	$(DOCKER_COMPOSE) up -d

docker-down:
	$(DOCKER_COMPOSE) down

docker-logs:
	$(DOCKER_COMPOSE) logs -f

docker-restart:
	$(DOCKER_COMPOSE) down
	$(DOCKER_COMPOSE) up -d --build
