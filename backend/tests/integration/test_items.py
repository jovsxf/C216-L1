import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.base import Base
from app.database.session import get_db
from app.main import app

test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSession = sessionmaker(bind=test_engine, autoflush=False, autocommit=False)


def override_get_db():
    with TestingSession() as db:
        yield db


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_items():
    Base.metadata.create_all(test_engine)
    yield
    Base.metadata.drop_all(test_engine)


@pytest.fixture(autouse=True)
def override_database():
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()


def test_get_items():
    response = client.get("/items/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_post_item():
    response = client.post(
        "/items/",
        json={
            "name": "Notebook",
            "description": "Notebook para estudos",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Notebook"
    assert data["description"] == "Notebook para estudos"
    assert "id" in data


def test_get_item():
    create_response = client.post(
        "/items/",
        json={
            "name": "Mouse",
            "description": "Mouse sem fio",
        },
    )

    item_id = create_response.json()["id"]

    response = client.get(f"/items/{item_id}")

    assert response.status_code == 200
    assert response.json()["id"] == item_id


def test_get_nonexistent_item():
    response = client.get("/items/99999")

    assert response.status_code == 404


def test_put_item():
    create_response = client.post(
        "/items/",
        json={
            "name": "Notebook",
            "description": "Descrição antiga",
        },
    )

    item_id = create_response.json()["id"]

    response = client.put(
        f"/items/{item_id}",
        json={
            "name": "Notebook atualizado",
            "description": "Nova descrição",
        },
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Notebook atualizado"


def test_patch_item():
    create_response = client.post(
        "/items/",
        json={
            "name": "Notebook",
            "description": "Descrição antiga",
        },
    )

    item_id = create_response.json()["id"]

    response = client.patch(
        f"/items/{item_id}",
        json={
            "description": "Descrição alterada",
        },
    )

    assert response.status_code == 200
    assert response.json()["description"] == "Descrição alterada"
    assert response.json()["name"] == "Notebook"


def test_delete_item():
    create_response = client.post(
        "/items/",
        json={
            "name": "Mouse",
            "description": "Mouse sem fio",
        },
    )

    item_id = create_response.json()["id"]

    response = client.delete(f"/items/{item_id}")

    assert response.status_code == 200

    get_response = client.get(f"/items/{item_id}")

    assert get_response.status_code == 404
