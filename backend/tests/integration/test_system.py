from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Backend funcionando!"}


def test_database_endpoint_success():
    connection = MagicMock()

    with patch("routes.system.psycopg2.connect", return_value=connection) as connect:
        response = client.get("/database")

    assert response.status_code == 200
    assert response.json() == {
        "database": "Conexão realizada com sucesso!",
    }
    connect.assert_called_once()
    connection.close.assert_called_once()


def test_database_endpoint_error():
    with patch(
        "routes.system.psycopg2.connect",
        side_effect=Exception("Banco de dados indisponível"),
    ):
        response = client.get("/database")

    assert response.status_code == 200
    assert response.json() == {
        "database": "Erro ao conectar ao banco",
        "error": "Banco de dados indisponível",
    }
