from pydantic import AliasChoices, BaseModel, Field

from src.mongo import PyObjectId


class Item(BaseModel):
    id: PyObjectId = Field(
        validation_alias=AliasChoices("id", "_id"), serialization_alias="id"
    )
    name: str
    price: float
    count: int


class ItemCreate(BaseModel):
    name: str
    price: float
    count: int


class ItemCreated(BaseModel):
    id: PyObjectId


class ItemUpdate(BaseModel):
    name: str | None = Field(None)
    price: float | None = Field(None)
    count: int | None = Field(None)


class ItemCollection(BaseModel):
    items: list[Item]

