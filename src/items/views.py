from typing import Any

from fastapi import APIRouter
from pydantic import NonNegativeInt

from src.mongo import PyObjectId

from .dependencies import ItemsServiceDep
from .exceptions import ItemNotFound
from .schemas import Item, ItemCollection, ItemCreate, ItemCreated, ItemUpdate

router = APIRouter()


@router.get("/", response_model=ItemCollection)
async def get_items(
    service: ItemsServiceDep,
    offset: NonNegativeInt = 0,
    count: NonNegativeInt = 20,
) -> Any:
    return ItemCollection(items=await service.get_all(count, offset))


@router.get("/{item_id}")
async def get_item(item_id: PyObjectId, service: ItemsServiceDep) -> Item:
    found_item = await service.get(item_id)
    if not found_item:
        raise ItemNotFound()
    return found_item


@router.post("/")
async def create_item(new_item: ItemCreate, service: ItemsServiceDep) -> ItemCreated:
    id = await service.add(new_item)
    return ItemCreated(id=id)


@router.patch("/{item_id}")
async def update_item(
    item_id: PyObjectId, updated_item: ItemUpdate, service: ItemsServiceDep
) -> None:
    item = await service.get(item_id)
    if not item:
        raise ItemNotFound()

    await service.update(item.id, updated_item)


@router.delete("/{item_id}")
async def delete_item(item_id: PyObjectId, service: ItemsServiceDep) -> None:
    item = await service.get(item_id)
    if not item:
        raise ItemNotFound()

    await service.delete(item.id)
