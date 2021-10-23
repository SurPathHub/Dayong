# pylint: disable=R0903
"""
dayong.protos
~~~~~~~~~~~~~~~~~

Interfaces used within Dayong.

NOTE: We use protocol classes for structural subtyping.
"""
from typing import Any, Protocol

from sqlmodel.engine.result import ScalarResult

from dayong.models import Message


class MessageDBProto(Protocol):
    """Protocol for a generic database interface."""

    async def create_table(self) -> None:
        """Create physical message tables for all the message table models stored in
        `SQLModel.metadata`.
        """
        raise NotImplementedError

    async def add_row(self, table_model_object: Message) -> None:
        """Add a row to the message table.

        Args:
            table_model_object (Message): An instance of `dayong.models.Message` or one
            of its subclasses.
        """
        raise NotImplementedError

    async def remove_row(self, table_model_object: Message) -> None:
        """Remove a row from the message table.

        Args:
            table_model_object (Message): An instance of `dayong.models.Message` or one
            of its subclasses.
        """
        raise NotImplementedError

    async def get_row(self, table_model_object: Message) -> ScalarResult[Any]:
        """Get data from the message table.

        Args:
            table_model_object (Message): Instance of a message table model.

        Returns:
            ScalarResult: An `ScalarResult` object which contains a scalar value or
                sequence of scalar values.
        """
        raise NotImplementedError
