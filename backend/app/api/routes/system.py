from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from backend.app.database.session import engine

router = APIRouter(tags=["system"])


@router.get("/")
def home():
    return {"message": "Backend funcionando!"}


@router.get("/database")
def check_database():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {"database": "Conexão realizada com sucesso!"}

    except SQLAlchemyError as error:
        return {
            "database": "Erro ao conectar ao banco",
            "error": str(error),
        }
