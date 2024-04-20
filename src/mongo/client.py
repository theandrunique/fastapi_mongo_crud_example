import os

import motor.motor_asyncio
from pymongo.errors import ConnectionFailure

from src.config import settings
from src.logger import logger

client = motor.motor_asyncio.AsyncIOMotorClient(
    settings.MONGO_URL,
    uuidRepresentation="standard",
    serverSelectionTimeoutMS=5000,
)

db = client[settings.MONGO_DATABASE_NAME]


async def test_connection() -> None:
    try:
        server_info = await client.server_info()
        formatted_info = (
            f"Successfully connected to MongoDB at {client.address}.\n"
            f"Cluster info:\n"
            f"  - Version: {server_info['version']}\n"
            f"  - Git Version: {server_info['gitVersion']}\n"
            f"  - OpenSSL Running: {server_info['openssl']['running']}\n"
            f"  - Compiled with: {server_info['buildEnvironment']['cc']}\n"
            f"  - Storage Engines: {', '.join(server_info['storageEngines'])}\n"
        )
        logger.info(formatted_info)

    except ConnectionFailure as e:
        logger.error(f"Could not connect to MongoDB at {client.address}:\n{e}")
        os._exit(1)
