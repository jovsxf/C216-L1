from schemas.item import Item, ItemCreate, ItemUpdate


items: list[Item] = []
next_id = 1


def get_items() -> list[Item]:
    return items


def get_item(item_id: int) -> Item | None:
    for item in items:
        if item.id == item_id:
            return item

    return None


def create_item(item_data: ItemCreate) -> Item:
    global next_id

    item = Item(
        id=next_id,
        name=item_data.name,
        description=item_data.description,
    )

    items.append(item)
    next_id += 1

    return item


def update_item(item_id: int, item_data: ItemCreate) -> Item | None:
    item = get_item(item_id)

    if item is None:
        return None

    item.name = item_data.name
    item.description = item_data.description

    return item


def patch_item(item_id: int, item_data: ItemUpdate) -> Item | None:
    item = get_item(item_id)

    if item is None:
        return None

    if item_data.name is not None:
        item.name = item_data.name

    if item_data.description is not None:
        item.description = item_data.description

    return item


def delete_item(item_id: int) -> bool:
    item = get_item(item_id)

    if item is None:
        return False

    items.remove(item)
    return True