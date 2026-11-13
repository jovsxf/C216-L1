from pydantic import BaseModel, Field

NAME_MAX_LENGTH = 100


class Item(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    name: str
    description: str | None = None


class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=NAME_MAX_LENGTH)
    description: str | None = None


class ItemUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=NAME_MAX_LENGTH)
    description: str | None = None


# Nome usado no material da Prática 7 para o schema de saída.
ItemRead = Item
