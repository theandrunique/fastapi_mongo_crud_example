import pytest

from src.items.dependencies import get_service
from src.items.schemas import Item, ItemCreate
from src.items.service import ItemsService
from src.main import app
from tests.base_fake_repo import BaseFakeRepository


class FakeItemsRepository(BaseFakeRepository):
    ...

@pytest.fixture(autouse=True)
def patch_mongo() -> ItemsService:
    repository = FakeItemsRepository()
    items_service = ItemsService(repository=repository) # pyright: ignore

    def fake_mongo_dep() -> BaseFakeRepository:
        return items_service

    app.dependency_overrides[get_service] = fake_mongo_dep
    return items_service


@pytest.fixture
async def prepare_test_element(patch_mongo) -> Item:
    test_item = ItemCreate(
        name="Foo",
        price=35.4,
        count=100,
    )
    id = await patch_mongo.add(test_item)
    return Item(**test_item.model_dump(), id=id)
