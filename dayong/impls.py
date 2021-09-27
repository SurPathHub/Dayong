"""
dayong.impls
~~~~~~~~~~~~

Implementaion of interfaces and the logic for injecting them.
"""
import asyncio
from typing import Optional

import tanjun
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession, ScalarResult

from dayong.configs import DayongConfig, DayongConfigLoader
from dayong.models import Message


class MessageDBImpl:
    """Implementaion of a database connection for transacting and interacting with
    message tables, those of which derive from message table models.

    The data to be selected, retrieved, and modified is determined by the table model
    object and its type. The type, in this case, is `dayong.models.Message`.
    """

    def __init__(self, database_uri: Optional[str] = None) -> None:
        self.engine = create_async_engine(
            database_uri if database_uri else DayongConfigLoader.load().database_uri
        )

    async def create_table(self) -> None:
        """Create physical message tables for all the message table models stored in
        `SQLModel.metadata`.
        """
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def add_row(self, tabe_model_object: Message) -> None:
        """Insert a row in the message table.

        Args:
            table_model_object (Message): An instance of `dayong.models.Message` or one
            of its subclasses.
        """
        async with AsyncSession(self.engine) as session:
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
        async with AsyncSession(self.engine) as session:
            # Temp ignore incompatible type passed to `exec()`. See:
            # https://github.com/tiangolo/sqlmodel/issues/54
            # https://github.com/tiangolo/sqlmodel/pull/58
            row: ScalarResult = await session.exec(
                select(table_model).where(  # type: ignore
                    table_model.message_id == tabe_model_object.message_id
                )
            )
            await session.delete(row)
            await session.commit()

    async def get_row(self, tabe_model_object: Message) -> ScalarResult:
        """Fetch a row from the message table.

        Args:
            tabe_model_object (Message): An instance of `dayong.models.Message` or one
            of its subclasses.

        Returns:
            ScalarResult: An `ScalarResult` object which contains a scalar value or
                sequence of scalar values.
        """
        table_model = type(tabe_model_object)
        async with AsyncSession(self.engine) as session:
            # Temp ignore incompatible type passed to `exec()`. See:
            # https://github.com/tiangolo/sqlmodel/issues/54
            # https://github.com/tiangolo/sqlmodel/pull/58
            row: ScalarResult = await session.exec(
                select(table_model).where(  # type: ignore
                    table_model.message_id == tabe_model_object.message_id
                )
            )
        return row

    @classmethod
    async def connect(
        cls,
        config: DayongConfig = tanjun.injected(type=DayongConfig),
    ) -> "MessageDBImpl":
        """Constuct an instance of `dayong.impls.MessageDBImpl`. This is used to
        register `MessageDBImpl` as a type dependency.

        Args:
            config (DayongConfig, optional): The config class to use. Defaults to
                `tanjun.injected(type=DayongConfig)`.

        Returns:
            MessageDBImpl: An instance `dayong.impls.MessageDBImpl`.
        """
        return cls(database_uri=config.database_uri)
