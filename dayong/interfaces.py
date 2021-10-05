# pylint: disable=R0903
"""
dayong.interfaces
~~~~~~~~~~~~~~~~~

Interfaces used within Dayong.

NOTE: We use protocol classes for structural subtyping.
"""
from typing import Any, Protocol

from sqlmodel.engine.result import ScalarResult

from dayong.models import Message


class GuildConfig(Protocol):
    """Protocol class for guild configuration."""

    @property
    def prefixes(self) -> list[str]:
        """Prefixes used by the guild.

        Returns:
            list[str]: Sequence of prefixes.
        """


class UserInfo(Protocol):
    """Protocol for user information."""


class MessageDBProto(Protocol):
    """Protocol for a generic database interface."""

    async def create_table(self) -> None:
        """Create physical message tables for all the message table models stored in
        `SQLModel.metadata`.
        """

    async def add_row(self, table_model_object: Message) -> None:
        """Add a row to the message table.

        Args:
            table_model_object (Message): An instance of `dayong.models.Message` or one
            of its subclasses.
        """

    async def remove_row(self, table_model_object: Message) -> None:
        """Remove a row from the message table.

        Args:
            table_model_object (Message): An instance of `dayong.models.Message` or one
            of its subclasses.
        """

    async def get_row(self, tabe_model_object: Message) -> ScalarResult[Any]:
        """Get data from the message table.

        Args:
            table_model_object (Message): Instance of a message table model.

        Returns:
            ScalarResult: An `ScalarResult` object which contains a scalar value or
                sequence of scalar values.
        """
