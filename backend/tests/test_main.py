import pytest
from unittest.mock import MagicMock, patch

from main import check_database, home


@pytest.fixture
def mock_connection():
    """Cria uma conexão simulada com o banco de dados."""
    connection = MagicMock()
    return connection


def test_home_returns_success_message():
    response = home()

    assert response == {"message": "Backend funcionando!"}


@pytest.mark.parametrize(
    "database_host,database_port",
    [
        ("localhost", "5432"),
        ("database", "5432"),
        ("127.0.0.1", "5433"),
    ],
)
def test_database_uses_environment_configuration(
    monkeypatch,
    mock_connection,
    database_host,
    database_port,
):
    monkeypatch.setenv("DATABASE_HOST", database_host)
    monkeypatch.setenv("DATABASE_PORT", database_port)

    with patch("main.psycopg2.connect", return_value=mock_connection) as mock_connect:
        response = check_database()

    assert response["database"] == "Conexão realizada com sucesso!"
    mock_connect.assert_called_once()

    connection_params = mock_connect.call_args.kwargs

    assert connection_params["host"] == database_host
    assert connection_params["port"] == database_port


def test_database_connection_success(mock_connection):
    with patch("main.psycopg2.connect", return_value=mock_connection):
        response = check_database()

    assert response["database"] == "Conexão realizada com sucesso!"


def test_database_connection_is_closed(mock_connection):
    with patch("main.psycopg2.connect", return_value=mock_connection):
        check_database()

    mock_connection.close.assert_called_once()


def test_database_connection_error():
    error_message = "Banco de dados indisponível"

    with patch(
        "main.psycopg2.connect",
        side_effect=Exception(error_message),
    ):
        response = check_database()

    assert response["database"] == "Erro ao conectar ao banco"
    assert response["error"] == error_message