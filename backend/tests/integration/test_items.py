from fastapi.testclient import TestClient
import pytest

from main import app
from services import item_service


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_items():
    item_service.items.clear()
    item_service.next_id = 1


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
