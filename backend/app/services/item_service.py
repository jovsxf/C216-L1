from sqlalchemy.orm import Session

from backend.app.repositories.item_repository import ItemRepository
from backend.app.schemas.item import ItemCreate, ItemUpdate


def get_items(db: Session):
    return ItemRepository(db).get_all()


def get_item(db: Session, item_id: int):
    return ItemRepository(db).get(item_id)


def create_item(db: Session, item_data: ItemCreate):
    return ItemRepository(db).create(**item_data.model_dump())


def update_item(db: Session, item_id: int, item_data: ItemCreate):
    repository = ItemRepository(db)
    item = repository.get(item_id)
    if item is None:
        return None
    return repository.update(item, **item_data.model_dump())


def patch_item(db: Session, item_id: int, item_data: ItemUpdate):
    repository = ItemRepository(db)
    item = repository.get(item_id)
    if item is None:
        return None
    changes = item_data.model_dump(exclude_unset=True)
    return repository.update(item, **changes) if changes else item


def delete_item(db: Session, item_id: int) -> bool:
    repository = ItemRepository(db)
    item = repository.get(item_id)
    if item is None:
        return False
    repository.delete(item)
    return True
