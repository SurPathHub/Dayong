# pylint: disable=R0903
"""
dayong.abc
~~~~~~~~~~

Interfaces used within Dayong.
"""

from abc import ABC, abstractmethod
from typing import Any

import tanjun
from sqlmodel import SQLModel
from sqlmodel.engine.result import ScalarResult

from dayong.core.configs import DayongConfig


class Database(ABC):
    """Abstract base class of a database interface."""

    @abstractmethod
    async def connect(
        self, config: DayongConfig = tanjun.injected(type=DayongConfig)
    ) -> None:
        """Create a database connection.

        Args:
            config (DayongConfig, optional): . Defaults to
                tanjun.injected(type=DayongConfig).
        """

    @abstractmethod
    async def create_table(self) -> None:
        """Create physical tables for all the table models stored in `Any.metadata`."""

    @abstractmethod
    async def add_row(self, table_model: SQLModel) -> None:
        """Add a row to the message table.

        Args:
            table_model (Any): A subclass of SQLModel
        """

    @abstractmethod
    async def remove_row(self, table_model: SQLModel, attribute: str) -> None:
        """Remove a row from the message table.

        Args:
            table_model (Any): A subclass of SQLModel
            attribute (str): A Table model attribute.
        """

    @abstractmethod
    async def get_row(self, table_model: SQLModel, attribute: str) -> ScalarResult[Any]:
        """Get row from the message table.

        Args:
            table_model (Any): A subclass of SQLModel.
            attribute (str): A Table model attribute.

        Returns:
            ScalarResult[Any]: A `ScalarResult` which contains a scalar value or
                sequence of scalar values.
        """

    @abstractmethod
    async def get_all_row(self, table_model: type[SQLModel]) -> ScalarResult[Any]:
        """Fetch all records in a database table.

        Args:
            table_model (type[SQLModel]): Type of the class which corresponds to a
                database table.
        Returns:
            ScalarResult[Any]: A `ScalarResult` which contains a scalar value or
                sequence of scalar values.
        """

    @abstractmethod
    async def update_row(self, table_model: SQLModel, attribute: str) -> None:
        """Update a database record/row.

        Args:
            table_model (Any): A subclass of SQLModel.
            attribute (str): A Table model attribute.
        """
