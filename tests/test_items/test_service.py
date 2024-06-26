from uuid import uuid4

import pytest

from src.items.exceptions import ItemNotFound
from src.items.models import ItemSchema
from src.items.schemas import ItemCreate, ItemUpdate


async def test_add_item(service, fake_repository, faker):
    item_create = ItemCreate(
        name=faker.name(),
        price=faker.random_number(digits=2),
        count=faker.random_int(1, 100),
    )
    expected_item = ItemSchema(
        id=uuid4(),
        name=item_create.name,
        price=item_create.price,
        count=item_create.count,
    )
    fake_repository.add.return_value = expected_item

    result = await service.add(item_create)

    assert result == expected_item
    fake_repository.add.assert_called_once_with(
        name=item_create.name,
        price=item_create.price,
        count=item_create.count,
    )


async def test_get_all_items(service, fake_repository, faker):
    items = [
        ItemSchema(
            id=uuid4(),
            name=faker.name(),
            price=faker.random_number(digits=2),
            count=faker.random_int(min=1, max=100),
        )
        for _ in range(10)
    ]

    total_count = len(items)
    fake_repository.get_many.return_value = (items, total_count)

    result, count = await service.get_all(count=10, offset=0)

    assert result == items
    assert count == total_count
    fake_repository.get_many.assert_called_once_with(10, 0)


async def test_get_item(service, fake_repository, faker):
    item_id = uuid4()
    expected_item = ItemSchema(
        id=item_id,
        name=faker.name(),
        price=faker.random_number(2),
        count=faker.random_int(1, 100),
    )
    fake_repository.get.return_value = expected_item

    result = await service.get(item_id)

    assert result == expected_item
    fake_repository.get.assert_called_once_with(item_id)


async def test_get_item_not_found(service, fake_repository):
    item_id = uuid4()
    fake_repository.get.return_value = None

    result = await service.get(item_id)

    assert result is None
    fake_repository.get.assert_called_once_with(item_id)


async def test_update_item(service, fake_repository, faker):
    item_id = uuid4()

    existing_item = ItemSchema(
        id=item_id,
        name=faker.name(),
        price=faker.random_number(digits=2),
        count=faker.random_int(min=1, max=100),
    )
    updated_values = ItemUpdate(
        name=faker.name(),
        price=faker.random_number(digits=2),
        count=faker.random_int(min=1, max=100),
    )
    updated_item = ItemSchema(
        id=item_id,
        name=updated_values.name,  # type: ignore
        price=updated_values.price,  # type: ignore
        count=updated_values.count,  # type: ignore
    )

    fake_repository.get.return_value = existing_item
    fake_repository.update.return_value = updated_item

    await service.update(item_id, updated_values)

    fake_repository.get.assert_called_once_with(item_id)
    fake_repository.update.assert_called_once_with(item_id, existing_item)


async def test_update_item_not_found(service, fake_repository, faker):
    item_id = uuid4()
    updated_values = ItemUpdate(
        name=faker.name(),
        price=faker.random_number(digits=2),
        count=faker.random_int(min=1, max=100),
    )
    fake_repository.get.return_value = None

    with pytest.raises(ItemNotFound):
        await service.update(item_id, updated_values)

    fake_repository.get.assert_called_once_with(item_id)
    fake_repository.update.assert_not_called()


async def test_delete_item(service, fake_repository, faker):
    item_id = uuid4()
    existing_item = ItemSchema(
        id=item_id,
        name=faker.name(),
        price=faker.random_number(digits=2),
        count=faker.random_int(min=1, max=100),
    )

    fake_repository.get.return_value = existing_item

    await service.delete(item_id)

    fake_repository.get.assert_called_once_with(item_id)
    fake_repository.delete.assert_called_once_with(item_id)


async def test_delete_item_not_found(service, fake_repository):
    item_id = uuid4()
    fake_repository.get.return_value = None

    with pytest.raises(ItemNotFound):
        await service.delete(item_id)

    fake_repository.get.assert_called_once_with(item_id)
    fake_repository.delete.assert_not_called()
