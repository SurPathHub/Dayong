"""
dayong.impls
~~~~~~~~~~~~

Implementaion of interfaces and the logic for injecting them.

NOTE: Explicitly declare that a class implements an interface.
"""
import asyncio
from typing import Optional

import tanjun
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession, ScalarResult

from dayong.configs import DayongConfig, DayongConfigLoader
from dayong.interfaces import MessageDBProto
from dayong.models import Message


class MessageDBImpl(MessageDBProto):
    """Implementaion of a connection to database message tables derived from message
    table models.
    """

    def __init__(self, database_uri: Optional[str] = None) -> None:
        self.engine = create_async_engine(
            database_uri if database_uri else DayongConfigLoader.load().database_uri
        )

    async def create_table(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def add_row(self, tabe_model_object: Message) -> None:
        async with AsyncSession(self.engine) as session:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, session.add, tabe_model_object)
            await session.commit()

    async def remove_row(self, tabe_model_object: Message) -> None:
        table_model = type(tabe_model_object)
        async with AsyncSession(self.engine) as session:
            # Temp ignore incompatible passed to `exec`. See:
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
        table_model = type(tabe_model_object)
        async with AsyncSession(self.engine) as session:
            # Temp ignore incompatible passed to `exec`. See:
            # https://github.com/tiangolo/sqlmodel/issues/54
            # https://github.com/tiangolo/sqlmodel/pull/58
            row: ScalarResult = await session.exec(
                select(table_model).where(  # type: ignore
                    table_model.message_id == tabe_model_object.message_id
                )
            )
        return row

    @classmethod
    async def connect(cls, config: DayongConfig = tanjun.injected(type=DayongConfig)):
        return cls(database_uri=config.database_uri)
