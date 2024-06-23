from dataclasses import dataclass
from typing import Annotated, Any

import bson
from fastapi import Query
from fastapi.params import Depends
from pydantic import (
    BaseModel,
    GetCoreSchemaHandler,
    GetJsonSchemaHandler,
    NonNegativeInt,
)
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, core_schema


class PyObjectId(bson.ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        def validate(value: str) -> PyObjectId:
            if not PyObjectId.is_valid(value):
                raise ValueError("Invalid ObjectId")
            return PyObjectId(value)

        return core_schema.no_info_plain_validator_function(
            function=validate,
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return handler(core_schema.str_schema())


class PaginationResponse[T](BaseModel):
    items: list[T]
    total: int
    offset: int
    count: int


@dataclass
class Pagination:
    offset: int
    count: int


def pagination_params(
    offset: NonNegativeInt = Query(0),
    count: NonNegativeInt = Query(20),
) -> Pagination:
    return Pagination(offset=offset, count=count)


PaginationParams = Annotated[Pagination, Depends(pagination_params)]
