from src.repositories.base.base_mongo_repository import BaseMongoRepository
from src.repositories.base.items import ItemsRepository
from src.schemas import PyObjectId


class MongoItemsRepository(BaseMongoRepository[PyObjectId], ItemsRepository): ...
