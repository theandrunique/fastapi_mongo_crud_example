from uuid import UUID, uuid4

from beanie import Document
from pydantic import BaseModel, Field
from sqlalchemy.orm import Mapped

from src.models import BaseORM


class ItemSchema(BaseModel):
    id: UUID
    name: str
    price: float
    count: int


class ItemORM(BaseORM):
    __tablename__ = "items"

    name: Mapped[str]
    price: Mapped[float]
    count: Mapped[int]


class ItemODM(Document):
    id: UUID = Field(default_factory=uuid4)  # type: ignore
    name: str
    price: float
    count: int  # type: ignore
