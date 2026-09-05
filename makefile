BACKEND_DIR=backend
POETRY=py -m poetry

.PHONY: help install run test check

help:
	@echo "Comandos disponíveis:"
	@echo "  make install - Instala as dependências"
	@echo "  make run     - Executa a aplicação"
	@echo "  make test    - Executa os testes"
	@echo "  make check   - Verifica a configuração do Poetry"

install:
	cd $(BACKEND_DIR) && $(POETRY) install

run:
	cd $(BACKEND_DIR) && $(POETRY) run uvicorn main:app --reload

test:
	cd $(BACKEND_DIR) && $(POETRY) run pytest

check:
	cd $(BACKEND_DIR) && $(POETRY) check