# pylint: disable=R0903
"""
dayong.abc
~~~~~~~~~~

Object interfaces used within Dayong.
"""

from abc import ABC, abstractmethod
from typing import Any

from sqlmodel.engine.result import ScalarResult


class Client(ABC):
    """Interface for a client class supporting any third-party service."""

    @staticmethod
    @abstractmethod
    async def get_content(data: Any, *args: Any, **kwargs: Any) -> Any:
        """Parse response data from a web request for specific content or detail.

        Returns:
            Any: Part of the response data.
        """
        raise NotImplementedError


class DBProto(ABC):
    """Protocol for a generic database interface."""

    @abstractmethod
    async def create_table(self) -> None:
        """Create physical message tables for all the message table models stored in
        `Any.metadata`.
        """
        raise NotImplementedError

    @abstractmethod
    async def add_row(self, table_model_object: Any) -> None:
        """Add a row to the message table.

        Args:
            table_model_object (Any): An instance of `dayong.models.Any` or one
            of its subclasses.
        """
        raise NotImplementedError

    @abstractmethod
    async def remove_row(self, table_model_object: Any) -> None:
        """Remove a row from the message table.

        Args:
            table_model_object (Any): An instance of `dayong.models.Any` or one
            of its subclasses.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_row(self, table_model_object: Any) -> ScalarResult[Any]:
        """Get data from the message table.

        Args:
            table_model_object (Any): Instance of a message table model.

        Returns:
            ScalarResult: An `ScalarResult` object which contains a scalar value or
                sequence of scalar values.
        """
        raise NotImplementedError
