# pylint: disable=R0903
"""
dayong.abc
~~~~~~~~~~

Interfaces used within Dayong.
"""

from abc import ABC, abstractmethod
from typing import Any

import tanjun
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
            config (DayongConfig, optional): [description]. Defaults to
                tanjun.injected(type=DayongConfig).
        """

    @abstractmethod
    async def create_table(self) -> None:
        """Create physical tables for all the table models stored in `Any.metadata`."""

    @abstractmethod
    async def add_row(self, table_model: Any) -> None:
        """Add a row to the message table.

        Args:
            table_model (Any): A subclass of SQLModel
        """

    @abstractmethod
    async def remove_row(self, table_model: Any) -> None:
        """Remove a row from the message table.

        Args:
            table_model (Any): A subclass of SQLModel
        """

    @abstractmethod
    async def get_row(self, table_model: Any) -> ScalarResult[Any]:
        """Get row from the message table.

        Args:
            table_model (Any): A subclass of SQLModel.

        Returns:
            ScalarResult: A `ScalarResult` which contains a scalar value or sequence of
                scalar values.
        """
