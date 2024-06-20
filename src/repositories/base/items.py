from abc import ABC, abstractmethod
from typing import Any

from src.schemas import PyObjectId


class ItemsRepository(ABC):
    @abstractmethod
    async def add(self, item: dict[str, Any]) -> PyObjectId: ...

    @abstractmethod
    async def get(self, id: PyObjectId) -> dict[str, Any] | None: ...

    @abstractmethod
    async def get_many(self, count: int, offset: int) -> list[dict[str, Any]]: ...

    @abstractmethod
    async def update(
        self, id: PyObjectId, new_values: dict[str, Any]
    ) -> dict[str, Any]: ...

    @abstractmethod
    async def delete(self, id: PyObjectId) -> int: ...
