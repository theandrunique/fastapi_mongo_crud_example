from uuid import UUID

from pydantic import BaseModel


class ItemSchema(BaseModel):
    id: UUID
    name: str
    price: float
    count: int


class ItemCreate(BaseModel):
    name: str
    price: float
    count: int


class ItemUpdate(BaseModel):
    name: str
    price: float
    count: int
