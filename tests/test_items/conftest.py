
from unittest.mock import AsyncMock

import pytest

from src.items.service import ItemsService
from src.repositories.base.items import ItemsRepository


@pytest.fixture
async def fake_repository():
    repo = AsyncMock(spec=ItemsRepository)
    return repo


@pytest.fixture
async def service(fake_repository):
    return ItemsService(repository=fake_repository)
