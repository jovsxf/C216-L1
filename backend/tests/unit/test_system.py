from unittest.mock import MagicMock, patch

from sqlalchemy.exc import SQLAlchemyError

from backend.app.API.system import check_database, home


def test_home_returns_success_message():
    assert home() == {"message": "Backend funcionando!"}


def test_database_connection_success():
    connection = MagicMock()
    context = MagicMock()
    context.__enter__.return_value = connection
    with patch("routes.system.engine.connect", return_value=context) as connect:
        response = check_database()
    assert response == {"database": "Conexão realizada com sucesso!"}
    connect.assert_called_once()
    connection.execute.assert_called_once()


def test_database_connection_error():
    with patch(
        "routes.system.engine.connect",
        side_effect=SQLAlchemyError("Banco de dados indisponível"),
    ):
        response = check_database()
    assert response == {
        "database": "Erro ao conectar ao banco",
        "error": "Banco de dados indisponível",
    }
