import os

import psycopg2
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Backend funcionando!"}


@app.get("/database")
def check_database():
    try:
        connection = psycopg2.connect(
            host=os.getenv("DATABASE_HOST", "localhost"),
            port=os.getenv("DATABASE_PORT", "5432"),
            dbname=os.getenv("DATABASE_NAME", "c216_db"),
            user=os.getenv("DATABASE_USER", "postgres"),
            password=os.getenv("DATABASE_PASSWORD", "postgres"),
        )

        connection.close()

        return {"database": "Conexão realizada com sucesso!"}

    except Exception as error:
        return {
            "database": "Erro ao conectar ao banco",
            "error": str(error),
        }