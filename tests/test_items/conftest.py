import pytest

from src.items.dependencies import get_repository
from src.items.schemas import Item, ItemCreate
from src.main import app
from tests.test_items.fake_repository import FakeItemRepository


@pytest.fixture(autouse=True)
def patch_mongo() -> FakeItemRepository:
    repository = FakeItemRepository()
    def fake_mongo_dep() -> FakeItemRepository:
        return repository

    app.dependency_overrides[get_repository] = fake_mongo_dep
    return repository


@pytest.fixture
async def prepare_test_element(patch_mongo) -> Item:
    test_item = ItemCreate(
        name="Foo",
        price=35.4,
        count=100,
    )
    return await patch_mongo.add(test_item)
