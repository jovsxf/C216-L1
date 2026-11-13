import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.base import Base
from app.schemas.item import ItemCreate, ItemUpdate
from app.services import item_service


@pytest.fixture
def db():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    with session_factory() as session:
        yield session
    Base.metadata.drop_all(engine)
    engine.dispose()


def test_create_item(db):
    item = item_service.create_item(
        db, ItemCreate(name="Notebook", description="Notebook para estudos")
    )
    assert item.id == 1
    assert item.name == "Notebook"


def test_get_item(db):
    created = item_service.create_item(
        db, ItemCreate(name="Mouse", description="Mouse sem fio")
    )
    assert item_service.get_item(db, created.id) == created


def test_get_nonexistent_item(db):
    assert item_service.get_item(db, 999) is None


@pytest.mark.parametrize(
    "name,description",
    [("Notebook", "Estudos"), ("Teclado", "Mecânico"), ("Mouse", "Sem fio")],
)
def test_create_different_items(db, name, description):
    item = item_service.create_item(db, ItemCreate(name=name, description=description))
    assert item.name == name
    assert item.description == description


def test_patch_item(db):
    item = item_service.create_item(
        db, ItemCreate(name="Notebook", description="Antiga descrição")
    )
    updated = item_service.patch_item(
        db, item.id, ItemUpdate(description="Nova descrição")
    )
    assert updated.description == "Nova descrição"
    assert updated.name == "Notebook"


def test_delete_item(db):
    item = item_service.create_item(
        db, ItemCreate(name="Mouse", description="Mouse sem fio")
    )
    assert item_service.delete_item(db, item.id) is True
    assert item_service.get_item(db, item.id) is None


def test_create_item_with_duplicate_name_raises(db):
    item_service.create_item(db, ItemCreate(name="Notebook"))
    with pytest.raises(item_service.DuplicateItemNameError):
        item_service.create_item(db, ItemCreate(name="Notebook"))


def test_update_item_keeping_own_name_is_allowed(db):
    item = item_service.create_item(db, ItemCreate(name="Notebook"))
    updated = item_service.update_item(
        db, item.id, ItemCreate(name="Notebook", description="Nova")
    )
    assert updated.description == "Nova"
