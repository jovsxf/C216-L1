import pytest

from schemas.item import ItemCreate, ItemUpdate
from services import item_service


@pytest.fixture(autouse=True)
def reset_items():
    item_service.items.clear()
    item_service.next_id = 1


def test_create_item():
    item_data = ItemCreate(
        name="Notebook",
        description="Notebook para estudos",
    )

    item = item_service.create_item(item_data)

    assert item.id == 1
    assert item.name == "Notebook"


def test_get_item():
    item_data = ItemCreate(
        name="Mouse",
        description="Mouse sem fio",
    )

    created_item = item_service.create_item(item_data)

    item = item_service.get_item(created_item.id)

    assert item == created_item


def test_get_nonexistent_item():
    item = item_service.get_item(999)

    assert item is None


@pytest.mark.parametrize(
    "name,description",
    [
        ("Notebook", "Notebook para estudos"),
        ("Teclado", "Teclado mecânico"),
        ("Mouse", "Mouse sem fio"),
    ],
)
def test_create_different_items(name, description):
    item = item_service.create_item(
        ItemCreate(
            name=name,
            description=description,
        )
    )

    assert item.name == name
    assert item.description == description


def test_patch_item():
    item = item_service.create_item(
        ItemCreate(
            name="Notebook",
            description="Antiga descrição",
        )
    )

    updated = item_service.patch_item(
        item.id,
        ItemUpdate(description="Nova descrição"),
    )

    assert updated.description == "Nova descrição"
    assert updated.name == "Notebook"


def test_delete_item():
    item = item_service.create_item(
        ItemCreate(
            name="Mouse",
            description="Mouse sem fio",
        )
    )

    result = item_service.delete_item(item.id)

    assert result is True
    assert item_service.get_item(item.id) is None