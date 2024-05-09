from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass(kw_only=True)
class BaseMongoRepository(ABC):
    @abstractmethod
    async def add(self, item: Any) -> Any: ...

    @abstractmethod
    async def get_many(self, count: int, offset: int) -> list[Any]: ...

    @abstractmethod
    async def get(self, id: Any) -> Any: ...

    @abstractmethod
    async def update(self, id: Any, new_values: dict[str, Any]) -> dict[str, Any]: ...

    @abstractmethod
    async def delete(self, id: Any) -> int: ...
