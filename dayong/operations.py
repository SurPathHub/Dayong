"""
dayong.operations
~~~~~~~~~~~~~~~~~

Data model operations which include retrieval and update commands.
"""
import asyncio
from typing import Any

import tanjun
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel import SQLModel, select
from sqlmodel.engine.result import ScalarResult
from sqlmodel.ext.asyncio.session import AsyncSession

from dayong.abc import Database
from dayong.core.configs import DayongConfig, DayongDynamicLoader


class DatabaseImpl(Database):
    """Implementaion of a database connection for transacting and interacting with
    database tables —those that derive from SQLModel.
    """

    _conn: AsyncEngine

    @staticmethod
    async def update(instance: Any, update: Any) -> Any:
        """Overwrite value of class attribute.

        Args:
            instance (Any): A Class instance.
            update (Any): A dictionary containing the attributes to be overwritten.

        Returns:
            Any: A class instance with updated attribute values.
        """
        for key, value in update.items():
            setattr(instance, key, value)
        return instance

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

    async def add_row(self, table_model: SQLModel) -> None:
        async with AsyncSession(self._conn) as session:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, session.add, table_model)
            await session.commit()

    async def remove_row(self, table_model: SQLModel, attribute: str) -> None:
        model = type(table_model)
        async with AsyncSession(self._conn) as session:
            # Temp ignore incompatible type passed to `exec()`. See:
            # https://github.com/tiangolo/sqlmodel/issues/54
            # https://github.com/tiangolo/sqlmodel/pull/58
            row: ScalarResult[Any] = await session.exec(
                select(model).where(
                    getattr(model, attribute) == getattr(table_model, attribute)
                )  # type: ignore
            )
            await session.delete(row.one())
            await session.commit()

    async def get_row(self, table_model: SQLModel, attribute: str) -> ScalarResult[Any]:
        model = type(table_model)
        async with AsyncSession(self._conn) as session:
            # Temp ignore incompatible type passed to `exec()`. See:
            # https://github.com/tiangolo/sqlmodel/issues/54
            # https://github.com/tiangolo/sqlmodel/pull/58
            row: ScalarResult[Any] = await session.exec(
                select(model).where(
                    getattr(model, attribute) == getattr(table_model, attribute)
                )  # type: ignore
            )
        return row

    async def get_all_row(self, table_model: type[SQLModel]) -> ScalarResult[Any]:
        async with AsyncSession(self._conn) as session:
            return await session.exec(select(table_model))  # type: ignore

    async def update_row(self, table_model: SQLModel, attribute: str) -> None:
        loop = asyncio.get_running_loop()
        model = type(table_model)
        table = table_model.__dict__

        async with AsyncSession(self._conn) as session:
            row: ScalarResult[Any] = await session.exec(
                select(model).where(
                    getattr(model, attribute) == getattr(table_model, attribute)
                )  # type: ignore
            )
            task = row.one()
            task = await self.update(task, table)
            await loop.run_in_executor(None, session.add, task)
            await session.commit()
            await session.refresh(task)
