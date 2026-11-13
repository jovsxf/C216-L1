from sqlalchemy.orm import Session

from app.repositories.item_repository import ItemRepository
from app.schemas.item import ItemCreate, ItemUpdate

DUPLICATE_NAME_MESSAGE = "Já existe um item com esse nome"


class DuplicateItemNameError(Exception):
    def __init__(self, message: str = DUPLICATE_NAME_MESSAGE):
        super().__init__(message)
        self.message = message


def _ensure_unique_name(
    repository: ItemRepository, name: str, ignore_id: int | None = None
) -> None:
    existing = repository.get_by_name(name)
    if existing is not None and existing.id != ignore_id:
        raise DuplicateItemNameError()


def get_items(db: Session):
    return ItemRepository(db).get_all()


def get_item(db: Session, item_id: int):
    return ItemRepository(db).get(item_id)


def create_item(db: Session, item_data: ItemCreate):
    repository = ItemRepository(db)
    _ensure_unique_name(repository, item_data.name)
    return repository.create(**item_data.model_dump())


def update_item(db: Session, item_id: int, item_data: ItemCreate):
    repository = ItemRepository(db)
    item = repository.get(item_id)
    if item is None:
        return None
    _ensure_unique_name(repository, item_data.name, ignore_id=item_id)
    return repository.update(item, **item_data.model_dump())


def patch_item(db: Session, item_id: int, item_data: ItemUpdate):
    repository = ItemRepository(db)
    item = repository.get(item_id)
    if item is None:
        return None
    changes = item_data.model_dump(exclude_unset=True)
    if changes.get("name") is not None:
        _ensure_unique_name(repository, changes["name"], ignore_id=item_id)
    return repository.update(item, **changes) if changes else item


def delete_item(db: Session, item_id: int) -> bool:
    repository = ItemRepository(db)
    item = repository.get(item_id)
    if item is None:
        return False
    repository.delete(item)
    return True
