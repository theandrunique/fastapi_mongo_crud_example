from uuid import uuid4

import pytest

from src.items.models import ItemSchema
from src.items.schemas import ItemCreate, ItemUpdate


@pytest.mark.asyncio
async def test_add_item(service, fake_repository):
    item_create = ItemCreate(name="Test Item", price=100, count=5)
    expected_item = ItemSchema(id=uuid4(), name="Test Item", price=100, count=5)
    fake_repository.add.return_value = expected_item

    result = await service.add(item_create)

    assert result == expected_item
    fake_repository.add.assert_called_once_with(
        name=item_create.name,
        price=item_create.price,
        count=item_create.count,
    )


@pytest.mark.asyncio
async def test_get_all_items(service, fake_repository):
    items = [ItemSchema(id=uuid4(), name="Item 1", price=50, count=10),
             ItemSchema(id=uuid4(), name="Item 2", price=150, count=20)]
    total_count = len(items)
    fake_repository.get_many.return_value = (items, total_count)

    result, count = await service.get_all(count=10, offset=0)

    assert result == items
    assert count == total_count
    fake_repository.get_many.assert_called_once_with(10, 0)


@pytest.mark.asyncio
async def test_get_item(service, fake_repository):
    item_id = uuid4()
    expected_item = ItemSchema(id=item_id, name="Test Item", price=100, count=5)
    fake_repository.get.return_value = expected_item

    result = await service.get(item_id)

    assert result == expected_item
    fake_repository.get.assert_called_once_with(item_id)


@pytest.mark.asyncio
async def test_get_item_not_found(service, fake_repository):
    item_id = uuid4()
    fake_repository.get.return_value = None

    result = await service.get(item_id)

    assert result is None
    fake_repository.get.assert_called_once_with(item_id)


@pytest.mark.asyncio
async def test_update_item(service, fake_repository):
    item_id = uuid4()
    existing_item = ItemSchema(id=item_id, name="Old Item", price=100, count=5)
    updated_values = ItemUpdate(name="Updated Item", price=200, count=10)
    updated_item = ItemSchema(id=item_id, name="Updated Item", price=200, count=10)

    fake_repository.get.return_value = existing_item
    fake_repository.update.return_value = updated_item

    result = await service.update(item_id, updated_values)

    assert result == updated_item
    fake_repository.get.assert_called_once_with(item_id)
    fake_repository.update.assert_called_once_with(item_id, existing_item)


@pytest.mark.asyncio
async def test_update_item_not_found(service, fake_repository):
    item_id = uuid4()
    updated_values = ItemUpdate(name="Updated Item", price=200, count=10)
    fake_repository.get.return_value = None

    result = await service.update(item_id, updated_values)

    assert result is None
    fake_repository.get.assert_called_once_with(item_id)
    fake_repository.update.assert_not_called()


@pytest.mark.asyncio
async def test_delete_item(service, fake_repository):
    item_id = uuid4()
    existing_item = ItemSchema(id=item_id, name="Test Item", price=100, count=5)
    fake_repository.get.return_value = existing_item
    fake_repository.delete.return_value = True

    result = await service.delete(item_id)

    assert result is True
    fake_repository.get.assert_called_once_with(item_id)
    fake_repository.delete.assert_called_once_with(item_id)


@pytest.mark.asyncio
async def test_delete_item_not_found(service, fake_repository):
    item_id = uuid4()
    fake_repository.get.return_value = None

    result = await service.delete(item_id)

    assert result is False
    fake_repository.get.assert_called_once_with(item_id)
    fake_repository.delete.assert_not_called()
