"""
dayong.operations
~~~~~~~~~~~~~~~~~

This module contains data model operations which include retrieval and update commands.
"""
import asyncio
from typing import Any, Type

import tanjun
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel import SQLModel, select
from sqlmodel.engine.result import ScalarResult
from sqlmodel.ext.asyncio.session import AsyncSession

from dayong.abc import Database
from dayong.core.configs import DayongConfig, DayongDynamicLoader
from dayong.models import Message, ScheduledTask


class MessageDB(Database):
    """Implementaion of a database connection for transacting and interacting with
    message tables —those that derive from message table models.
    """

    _conn: AsyncEngine

    async def connect(
        self, config: DayongConfig = tanjun.injected(type=DayongConfig)
    ) -> None:
        """Create a database connection.

        Args:
            config (DayongConfig, optional): A config interface. Defaults to
                tanjun.injected(type=DayongConfig).
        """
        loop = asyncio.get_running_loop()
        self._conn = await loop.run_in_executor(
            None,
            create_async_engine,
            config.database_uri
            if config.database_uri
            else DayongDynamicLoader().load().database_uri,
        )

    async def create_table(self) -> None:
        async with self._conn.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def add_row(self, table_model: Message) -> None:
        async with AsyncSession(self._conn) as session:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, session.add, table_model)
            await session.commit()

    async def remove_row(self, table_model: Message) -> None:
        model = type(table_model)
        async with AsyncSession(self._conn) as session:
            # Temp ignore incompatible type passed to `exec()`. See:
            # https://github.com/tiangolo/sqlmodel/issues/54
            # https://github.com/tiangolo/sqlmodel/pull/58
            row: ScalarResult[Any] = await session.exec(
                select(model).where(model.id == table_model.id)  # type: ignore
            )
            await session.delete(row)
            await session.commit()

    async def get_row(self, table_model: Message) -> ScalarResult[Any]:
        model = type(table_model)
        async with AsyncSession(self._conn) as session:
            # Temp ignore incompatible type passed to `exec()`. See:
            # https://github.com/tiangolo/sqlmodel/issues/54
            # https://github.com/tiangolo/sqlmodel/pull/58
            row: ScalarResult[Any] = await session.exec(
                select(model).where(model.id == table_model.id)  # type: ignore
            )
        return row


class ScheduledTaskDB(Database):
    """Implements a database connection for managing scheduled tasks."""

    _conn: AsyncEngine

    async def connect(
        self, config: DayongConfig = tanjun.injected(type=DayongConfig)
    ) -> None:
        loop = asyncio.get_running_loop()
        self._conn = await loop.run_in_executor(
            None,
            create_async_engine,
            config.database_uri
            if config.database_uri
            else DayongDynamicLoader().load().database_uri,
        )

    async def create_table(self) -> None:
        async with self._conn.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def add_row(self, table_model: ScheduledTask) -> None:
        async with AsyncSession(self._conn) as session:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, session.add, table_model)
            await session.commit()

    async def remove_row(self, table_model: ScheduledTask) -> None:
        model = type(table_model)
        async with AsyncSession(self._conn) as session:
            row: ScalarResult[Any] = await session.exec(
                select(model).where(
                    model.channel_name == table_model.channel_name
                )  # type: ignore
            )
            await session.delete(row.one())
            await session.commit()

    async def get_row(self, table_model: ScheduledTask) -> ScalarResult[Any]:
        model = type(table_model)
        async with AsyncSession(self._conn) as session:
            row: ScalarResult[Any] = await session.exec(
                select(model).where(  # type: ignore
                    model.task_name == table_model.task_name
                )
            )
        return row

    async def get_all_row(self, table_model: Type[ScheduledTask]) -> ScalarResult[Any]:
        async with AsyncSession(self._conn) as session:
            return await session.exec(select(table_model))  # type: ignore

    async def update_row(self, table_model: ScheduledTask) -> None:
        loop = asyncio.get_running_loop()
        model = type(table_model)
        async with AsyncSession(self._conn) as session:
            row: ScalarResult[Any] = await session.exec(
                select(model).where(
                    model.channel_name == table_model.channel_name
                )  # type: ignore
            )
            task = row.one()
            if table_model.task_name:
                task.name = table_model.task_name
            if table_model.run:
                task.run = table_model.run
            await loop.run_in_executor(None, session.add, task)
            await session.commit()
            await session.refresh(task)
