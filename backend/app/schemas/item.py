from pydantic import BaseModel


class Item(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    name: str
    description: str


class ItemCreate(BaseModel):
    name: str
    description: str


class ItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
