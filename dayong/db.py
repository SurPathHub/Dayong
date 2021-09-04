"""
dayong.db
~~~~~~~~~

Database models, objects, and connections used within Dayong.
"""
from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import Field, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession


class TableModel(SQLModel):  # pylint: disable=R0903
    """Base class for database models."""


class AnonymousMessageTB(TableModel, table=True):
    """Table model for anonymous messages."""

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    username: str
    nickname: str
    message: str


class Database(ABC):
    """Common interface for Database objects."""

    @abstractmethod
    async def create_table(self) -> None:
        """Create database table."""

    @abstractmethod
    async def add_row(self, model: TableModel) -> None:
        """Add row to type of `db.TableModel`."""


class SQLDatabase(Database):
    """Class for handling SQL database connections."""

    def __init__(self, connection_uri: str):
        self.engine = create_async_engine(connection_uri)

    async def create_table(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def add_row(self, model: TableModel) -> None:
        async with AsyncSession(self.engine) as session:
            session.add(model)
            await session.commit()

    # To access data, see https://github.com/tiangolo/sqlmodel/pull/58
