from dataclasses import dataclass
from typing import Any

import bson
from fastapi import Query, params
from pydantic import (
    BaseModel,
    GetCoreSchemaHandler,
    GetJsonSchemaHandler,
    NonNegativeInt,
    PositiveInt,
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
    limit: int


@dataclass
class PaginationParams:
    offset: int
    limit: int


def Pagination() -> PaginationParams:
    async def dependency(
        offset: NonNegativeInt = Query(0),
        limit: PositiveInt = Query(20, le=100),
    ):
        return PaginationParams(offset=offset, limit=limit)

    return params.Depends(dependency=dependency, use_cache=True)  # type: ignore
