from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.item import Item


class ItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Item]:
        return list(self.db.scalars(select(Item).order_by(Item.id)).all())

    def get(self, item_id: int) -> Item | None:
        return self.db.get(Item, item_id)

    def create(self, name: str, description: str) -> Item:
        item = Item(name=name, description=description)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update(self, item: Item, **changes: str) -> Item:
        for field, value in changes.items():
            setattr(item, field, value)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item: Item) -> None:
        self.db.delete(item)
        self.db.commit()
