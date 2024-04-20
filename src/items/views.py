from typing import Any

from fastapi import APIRouter
from pydantic import NonNegativeInt

from src.mongo import PyObjectId

from .exceptions import ItemNotFound
from .repository import ItemRepository
from .schemas import Item, ItemCollection, ItemCreate, ItemUpdate

repository = ItemRepository()

router = APIRouter()


@router.get("/", response_model=ItemCollection)
async def get_items(offset: NonNegativeInt = 0, count: NonNegativeInt = 20) -> Any:
    return ItemCollection(items=await repository.get_all(count, offset))


@router.get("/{item_id}")
async def get_item(item_id: PyObjectId) -> Item:
    found_item = await repository.get(item_id)
    if not found_item:
        raise ItemNotFound()
    return found_item


@router.post("/")
async def create_item(new_item: ItemCreate) -> Item:
    return await repository.add(new_item)


@router.patch("/{item_id}")
async def update_item(item_id: PyObjectId, updated_item: ItemUpdate) -> Item:
    item = await repository.get(item_id)
    if not item:
        raise ItemNotFound()

    new_values = updated_item.model_dump(exclude_defaults=True)
    if new_values:
        return await repository.update(item.id, new_values)
    else:
        return item


@router.delete("/{item_id}")
async def delete_item(item_id: PyObjectId) -> None:
    item = await repository.get(item_id)
    if not item:
        raise ItemNotFound()

    await repository.delete(item.id)
