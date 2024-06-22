from dataclasses import dataclass
from uuid import UUID

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base


@dataclass
class Item:
    id: UUID
    name: str
    price: float
    count: int


class ItemModel(Base):
    __tablename__ = "items"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=sqlalchemy.text("gen_random_uuid ()"),
    )
    name: Mapped[str]
    price: Mapped[float]
    count: Mapped[int]


class ItemMongoModel: ...
