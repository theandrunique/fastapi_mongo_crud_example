import pytest

from src.container import container
from src.items.schemas import Item, ItemCreate
from src.items.service import ItemsService
from src.repositories.base.items import ItemsRepository
from tests.base_fake_repo import BaseFakeRepository


class FakeItemsRepository(BaseFakeRepository): ...


@pytest.fixture(autouse=True)
def patch_mongo() -> ItemsService:
    repository = FakeItemsRepository()

    container.register(ItemsRepository, instance=repository)

    return container.resolve(ItemsService) # type: ignore


@pytest.fixture
async def prepare_test_element(patch_mongo) -> Item:
    test_item = ItemCreate(
        name="Foo",
        price=35.4,
        count=100,
    )

    return await patch_mongo.add(test_item)
