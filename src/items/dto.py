from dataclasses import dataclass
from uuid import UUID

from src.dto import BaseDTO


@dataclass(frozen=True, slots=True)
class ItemDTO(BaseDTO):
    id: UUID
    name: str
    price: float
    count: int
