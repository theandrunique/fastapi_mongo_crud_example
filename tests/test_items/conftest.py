import pytest

from tests.test_items.fake_repository import FakeItemRepository


@pytest.fixture(autouse=True)
def patch_mongo(monkeypatch):
    fake_mongo = FakeItemRepository()
    monkeypatch.setattr("src.items.views.repository", fake_mongo)
