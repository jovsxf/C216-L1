from fastapi import APIRouter, HTTPException

from schemas.item import Item, ItemCreate, ItemUpdate
from services import item_service


router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=list[Item])
def list_items():
    return item_service.get_items()


@router.get("/{item_id}", response_model=Item)
def get_item(item_id: int):
    item = item_service.get_item(item_id)

    if item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    return item


@router.post("/", response_model=Item, status_code=201)
def create_item(item_data: ItemCreate):
    return item_service.create_item(item_data)


@router.put("/{item_id}", response_model=Item)
def update_item(item_id: int, item_data: ItemCreate):
    item = item_service.update_item(item_id, item_data)

    if item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    return item


@router.patch("/{item_id}", response_model=Item)
def patch_item(item_id: int, item_data: ItemUpdate):
    item = item_service.patch_item(item_id, item_data)

    if item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    return item


@router.delete("/{item_id}")
def delete_item(item_id: int):
    deleted = item_service.delete_item(item_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    return {"message": "Item removido com sucesso"}