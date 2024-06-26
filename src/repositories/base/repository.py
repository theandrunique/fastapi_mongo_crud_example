from abc import ABC, abstractmethod

from pydantic import BaseModel


class Repository[SchemaType: BaseModel, IDType](ABC):
    @abstractmethod
    async def add(self, **kwargs) -> SchemaType: ...

    @abstractmethod
    async def get(self, id: IDType) -> SchemaType | None: ...

    @abstractmethod
    async def get_many(
        self,
        count: int,
        offset: int,
    ) -> list[SchemaType]: ...

    @abstractmethod
    async def count(self) -> int: ...

    @abstractmethod
    async def update(self, id: IDType, updated_item: SchemaType): ...

    @abstractmethod
    async def delete(self, id: IDType) -> None: ...
