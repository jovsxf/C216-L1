from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

from app.main import app

client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Backend funcionando!"}


def test_database_endpoint_success():
    connection = MagicMock()
    context = MagicMock()
    context.__enter__.return_value = connection
    with patch("app.api.routes.system.engine.connect", return_value=context) as connect:
        response = client.get("/database")

    assert response.status_code == 200
    assert response.json() == {
        "database": "Conexão realizada com sucesso!",
    }
    connect.assert_called_once()
    connection.execute.assert_called_once()


def test_database_endpoint_error():
    with patch(
        "app.api.routes.system.engine.connect",
        side_effect=SQLAlchemyError("Banco de dados indisponível"),
    ):
        response = client.get("/database")

    assert response.status_code == 200
    assert response.json() == {
        "database": "Erro ao conectar ao banco",
        "error": "Banco de dados indisponível",
    }
