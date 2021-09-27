# pylint: disable=R0903
"""
dayong.interfaces
~~~~~~~~~~~~~~~~~

Interfaces used within Dayong.

NOTE: We use protocol classes for structural subtyping.
"""
from typing import Any, Protocol

from dayong.models import Message


class GuildConfig(Protocol):
    """Protocol class for guild configuration.

    Args:
        Protocol (Generic): The base class for Protocol classes.
    """

    @property
    def prefixes(self) -> list[str]:
        """Prefixes used by the guild.

        Returns:
            list[str]: Sequence of prefixes.
        """


class UserInfo(Protocol):
    """Protocol for user information.

    Args:
        Protocol (Generic): The base class for Protocol classes.
    """


class MessageDBProto(Protocol):
    """Protocol for a generic database interface.

    Args:
        Protocol (Generic): [description]
    """

    async def create_table(self) -> None:
        """Create physical message tables."""

    async def add_row(self, table_model_object: Message) -> None:
        """Add a row to the message table.

        Args:
            table_model_object (Message): Instance of a message table model.
        """

    async def remove_row(self, table_model_object: Message) -> None:
        """Remove a row from the message table.

        Args:
            table_model_object (Message): Instance of a message table model.
        """

    async def get_row(self, tabe_model_object: Message) -> Any:
        """Get data from the message table.

        Args:
            table_model_object (Message): Instance of a message table model.

        Returns:
            Any: A scalar value or sequence of scalar values.
        """
