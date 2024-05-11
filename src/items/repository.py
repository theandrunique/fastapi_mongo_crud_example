from dataclasses import dataclass

from src.mongo.base_repository import BaseMongoRepository
from src.mongo.object_id import PyObjectId


@dataclass(kw_only=True)
class ItemsRepository(BaseMongoRepository[PyObjectId]): ...
