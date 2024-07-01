from typing import Any
from uuid import UUID

from fastapi import APIRouter, status

from src.dependencies import Container, Provide
from src.schemas import Pagination, PaginationResponse

from .exceptions import ItemNotFound
from .schemas import ItemCreate, ItemSchema, ItemUpdate

router = APIRouter()


@router.get("", response_model=PaginationResponse[ItemSchema])
async def get_items(
    pagination=Pagination(),
    items_service=Provide(Container.ItemsService),
) -> Any:
    items, total = await items_service.get_all(pagination.limit, pagination.offset)
    return {
        "items": items,
        "limit": len(items),
        "offset": pagination.offset,
        "total": total,
    }


@router.get("/{item_id}", response_model=ItemSchema)
async def get_item(item_id: UUID, items_service=Provide(Container.ItemsService)) -> Any:
    found_item = await items_service.get(item_id)
    if not found_item:
        raise ItemNotFound()
    return found_item


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ItemSchema)
async def create_item(
    new_item_data: ItemCreate, items_service=Provide(Container.ItemsService)
) -> Any:
    new_item = await items_service.add(new_item_data)
    return new_item


@router.patch("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_item(
    item_id: UUID,
    updated_item: ItemUpdate,
    items_service=Provide(Container.ItemsService),
) -> None:
    item = await items_service.get(item_id)
    if not item:
        raise ItemNotFound()

    await items_service.update(item.id, updated_item)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: UUID, items_service=Provide(Container.ItemsService)
) -> None:
    item = await items_service.get(item_id)
    if not item:
        raise ItemNotFound()

    await items_service.delete(item.id)
