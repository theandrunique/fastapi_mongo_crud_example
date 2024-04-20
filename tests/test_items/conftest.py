import pytest

from src.items.schemas import Item, ItemCreate
from tests.test_items.fake_repository import FakeItemRepository


@pytest.fixture(autouse=True)
def patch_mongo(monkeypatch) -> FakeItemRepository:
    fake_mongo = FakeItemRepository()
    monkeypatch.setattr("src.items.views.repository", fake_mongo)
    return fake_mongo


@pytest.fixture
async def prepare_test_element(patch_mongo) -> Item:
    test_item = ItemCreate(
        name="Foo",
        price=35.4,
        count=100,
    )
    return await patch_mongo.add(test_item)
