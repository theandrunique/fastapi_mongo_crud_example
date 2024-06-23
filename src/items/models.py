from uuid import UUID, uuid4

import sqlalchemy
from beanie import Document
from pydantic import BaseModel, Field
from sqlalchemy.orm import Mapped, mapped_column

from src.models import BaseORM


class ItemSchema(BaseModel):
    id: UUID
    name: str
    price: float
    count: int


class ItemORM(BaseORM):
    __tablename__ = "items"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=sqlalchemy.text("gen_random_uuid()"),
    )
    name: Mapped[str]
    price: Mapped[float]
    count: Mapped[int]


class ItemODM(Document):
    id: UUID = Field(default_factory=uuid4)
    name: str
    price: float
    item_count: int
