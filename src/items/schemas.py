from pydantic import AliasChoices, BaseModel, Field

from src.mongo import PyObjectId


class ItemInMongo(BaseModel):
    id: PyObjectId = Field(
        validation_alias=AliasChoices("id", "_id"), serialization_alias="id"
    )
    name: str
    price: float
    count: int


class ItemCreateSchema(BaseModel):
    name: str
    price: float
    count: int


class ItemUpdateSchema(BaseModel):
    name: str | None = Field(None)
    price: float | None = Field(None)
    count: int | None = Field(None)


class ItemCollection(BaseModel):
    items: list[ItemInMongo]