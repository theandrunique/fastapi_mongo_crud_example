from typing import Any
from uuid import UUID

from fastapi import APIRouter
from pydantic import NonNegativeInt

from src.dependencies import Container, Provide

from .exceptions import ItemNotFound
from .schemas import ItemCollection, ItemCreate, ItemSchema, ItemUpdate

router = APIRouter()


@router.get("", response_model=ItemCollection)
async def get_items(
    items_service=Provide(Container.ItemsService),
    offset: NonNegativeInt = 0,
    count: NonNegativeInt = 20,
) -> Any:
    return ItemCollection(items=await items_service.get_all(count, offset))


@router.get("/{item_id}")
async def get_item(
    item_id: UUID, items_service=Provide(Container.ItemsService)
) -> ItemSchema:
    found_item = await items_service.get(item_id)
    if not found_item:
        raise ItemNotFound()
    return found_item


@router.post("")
async def create_item(
    new_item_data: ItemCreate, items_service=Provide(Container.ItemsService)
) -> ItemSchema:
    new_item = await items_service.add(new_item_data)
    return new_item


@router.patch("/{item_id}")
async def update_item(
    item_id: UUID,
    updated_item: ItemUpdate,
    items_service=Provide(Container.ItemsService),
) -> None:
    item = await items_service.get(item_id)
    if not item:
        raise ItemNotFound()

    await items_service.update(item.id, updated_item)


@router.delete("/{item_id}")
async def delete_item(
    item_id: UUID, items_service=Provide(Container.ItemsService)
) -> None:
    item = await items_service.get(item_id)
    if not item:
        raise ItemNotFound()

    await items_service.delete(item.id)
