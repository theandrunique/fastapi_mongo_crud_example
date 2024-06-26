from typing import Any

import pytest
from faker import Faker
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.database import DBHelper
from src.repositories.base.sqlalchemy_repository import SQLAlchemyRepository


class BaseORM(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class User(BaseORM):
    __tablename__ = "users"

    name: Mapped[str]


class UserSchema(BaseModel):
    id: int
    name: str


@pytest.fixture
def faker():
    return Faker()


@pytest.fixture
def random_user_schema(faker) -> dict[str, Any]:
    return {
        "name": faker.name(),
    }


@pytest.fixture(scope="function")
async def async_engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(BaseORM.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="function")
async def db_helper(async_engine):
    async_session = async_sessionmaker[AsyncSession](
        async_engine, class_=AsyncSession, expire_on_commit=False
    )
    db_helper = DBHelper(session_factory=async_session, engine=async_engine)
    return db_helper


@pytest.fixture(scope="function")
async def repository(db_helper):
    repo = SQLAlchemyRepository(db_helper=db_helper)
    repo.model = User
    repo.schema = UserSchema
    yield repo


async def test_add_item(repository, random_user_schema):
    new_item = await repository.add(**random_user_schema)
    assert new_item.name == random_user_schema["name"]


async def test_get_item(repository, random_user_schema):
    new_item = await repository.add(**random_user_schema)
    retrieved_item = await repository.get(new_item.id)
    assert retrieved_item is not None
    assert retrieved_item.name == random_user_schema["name"]


async def test_delete_item(repository, random_user_schema):
    new_item = await repository.add(**random_user_schema)
    await repository.delete(new_item.id)
    retrieved_item = await repository.get(new_item.id)
    assert retrieved_item is None


async def test_get_many_items(repository, faker):
    items = [await repository.add(name=faker.name()) for _ in range(5)]
    retrieved_items = await repository.get_many(count=5, offset=0)
    assert len(retrieved_items) == 5
    for item in items:
        assert any(retrieved_item.id == item.id for retrieved_item in retrieved_items)


async def test_update_item(repository, random_user_schema, faker):
    new_item = await repository.add(**random_user_schema)
    updated_name = faker.name()
    await repository.update(new_item.id, UserSchema(id=new_item.id, name=updated_name))
    updated_item = await repository.get(new_item.id)
    assert updated_item is not None
    assert updated_item.name == updated_name
