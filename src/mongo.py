import os
from typing import Any

import bson
import motor.motor_asyncio
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, core_schema
from pymongo.errors import ConnectionFailure

from src.config import settings
from src.logging import logger

mongo_client = motor.motor_asyncio.AsyncIOMotorClient(  # type: ignore
    settings.MONGO_URL, uuidRepresentation="standard",
    serverSelectionTimeoutMS=5000,
)

db = mongo_client[settings.MONGO_DATABASE_NAME]


async def test_connection() -> None:
    try:
        server_info = await mongo_client.server_info()
        formatted_info = (
            f"Successfully connected to MongoDB at {mongo_client.address}.\n"
            f"Cluster info:\n"
            f"  - Version: {server_info['version']}\n"
            f"  - Git Version: {server_info['gitVersion']}\n"
            f"  - OpenSSL Running: {server_info['openssl']['running']}\n"
            f"  - Compiled with: {server_info['buildEnvironment']['cc']}\n"
            f"  - Storage Engines: {', '.join(server_info['storageEngines'])}\n"
        )
        logger.info(formatted_info)

    except ConnectionFailure as e:
        logger.error(f"Could not connect to MongoDB at {mongo_client.address}:\n{e}")
        os._exit(1)


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
