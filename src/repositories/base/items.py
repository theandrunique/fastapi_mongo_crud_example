from abc import abstractmethod
from uuid import UUID

from src.items.models import ItemSchema


class ItemsRepository:
    @abstractmethod
    async def add(
        self,
        *,
        name: str,
        price: float,
        count: int,
    ) -> ItemSchema: ...

    @abstractmethod
    async def get(self, id: UUID) -> ItemSchema | None: ...

    @abstractmethod
    async def get_many(
        self, count: int, offset: int,
    ) -> tuple[list[ItemSchema], int]: ...

    @abstractmethod
    async def update(self, id: UUID, updated_item: ItemSchema): ...

    @abstractmethod
    async def delete(self, id: UUID) -> None: ...
