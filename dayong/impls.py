"""
dayong.impls
~~~~~~~~~~~~

Implementaion of interfaces and the logic for injecting them.
"""
import asyncio
from typing import Any

import tanjun
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel import SQLModel, select
from sqlmodel.engine.result import ScalarResult
from sqlmodel.ext.asyncio.session import AsyncSession

from dayong.configs import DayongConfig, DayongConfigLoader
from dayong.models import Message


class MessageDBImpl:
    """Implementaion of a database connection for transacting and interacting with
    message tables, those of which derive from message table models.

    The data to be selected, retrieved, and modified is determined by the table model
    object and its type. The type, in this case, is `dayong.models.Message`.
    """

    def __init__(self) -> None:
        self._conn: AsyncEngine

    async def connect(self, config: DayongConfig = tanjun.injected(type=DayongConfig)):
        """Create a database connection.

        If the `database_uri` is Falsy, the function will reattempt to get the url from
        the environment variables.

        Args:
            config (DayongConfig, optional): [description]. Defaults to
                tanjun.injected(type=DayongConfig).
        """
        loop = asyncio.get_running_loop()
        self._conn = await loop.run_in_executor(
            None,
            create_async_engine,
            config.database_uri if config.database_uri else DayongConfigLoader().load(),
        )

    async def create_table(self) -> None:
        """Create physical message tables for all the message table models stored in
        `SQLModel.metadata`.
        """
        async with self._conn.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def add_row(self, tabe_model_object: Message) -> None:
        """Insert a row in the message table.

        Args:
            table_model_object (Message): An instance of `dayong.models.Message` or one
            of its subclasses.
        """
        async with AsyncSession(self._conn) as session:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, session.add, tabe_model_object)
            await session.commit()

    async def remove_row(self, tabe_model_object: Message) -> None:
        """Delete a row in the message table.

        Args:
            table_model_object (Message): An instance of `dayong.models.Message` or one
            of its subclasses.
        """
        table_model = type(tabe_model_object)
        async with AsyncSession(self._conn) as session:
            # Temp ignore incompatible type passed to `exec()`. See:
            # https://github.com/tiangolo/sqlmodel/issues/54
            # https://github.com/tiangolo/sqlmodel/pull/58
            row: ScalarResult[Any] = await session.exec(
                select(table_model).where(  # type: ignore
                    table_model.message_id == tabe_model_object.message_id
                )
            )
            await session.delete(row)
            await session.commit()

    async def get_row(self, tabe_model_object: Message) -> ScalarResult[Any]:
        """Fetch a row from the message table.

        Args:
            tabe_model_object (Message): An instance of `dayong.models.Message` or one
            of its subclasses.

        Returns:
            ScalarResult: An `ScalarResult` object which contains a scalar value or
                sequence of scalar values.
        """
        table_model = type(tabe_model_object)
        async with AsyncSession(self._conn) as session:
            # Temp ignore incompatible type passed to `exec()`. See:
            # https://github.com/tiangolo/sqlmodel/issues/54
            # https://github.com/tiangolo/sqlmodel/pull/58
            row: ScalarResult[Any] = await session.exec(
                select(table_model).where(  # type: ignore
                    table_model.message_id == tabe_model_object.message_id
                )
            )
        return row
