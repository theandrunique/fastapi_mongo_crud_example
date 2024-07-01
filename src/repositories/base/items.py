from abc import abstractmethod
from uuid import UUID

from src.items.dto import ItemDTO


class ItemsRepository:
    @abstractmethod
    async def add(
        self,
        *,
        name: str,
        price: float,
        count: int,
    ) -> ItemDTO: ...

    @abstractmethod
    async def get(self, id: UUID) -> ItemDTO | None: ...

    @abstractmethod
    async def get_many(
        self,
        count: int,
        offset: int,
    ) -> list[ItemDTO]: ...

    @abstractmethod
    async def count(self) -> int: ...

    @abstractmethod
    async def update(self, id: UUID, updated_item: ItemDTO): ...

    @abstractmethod
    async def delete(self, id: UUID) -> None: ...
