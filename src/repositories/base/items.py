from abc import ABC, abstractmethod
from uuid import UUID

from src.items.models import Item


class ItemsRepository(ABC):
    @abstractmethod
    async def add(
        self,
        name: str,
        price: float,
        count: int,
    ) -> Item: ...

    @abstractmethod
    async def get(self, id: UUID) -> Item | None: ...

    @abstractmethod
    async def get_many(self, count: int, offset: int) -> list[Item]: ...

    @abstractmethod
    async def update(self, id: UUID, updated_item: Item): ...

    @abstractmethod
    async def delete(self, id: UUID) -> bool: ...
