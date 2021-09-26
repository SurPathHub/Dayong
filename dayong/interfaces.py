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
        ...


class UserInfo(Protocol):
    """Protocol for user information.

    Args:
        Protocol (Generic): The base class for Protocol classes.
    """

    ...


class MessageDBProto(Protocol):
    """Protocol for a generic database interface.

    Args:
        Protocol (Generic): [description]
    """

    async def create_table(self) -> None:
        ...

    async def add_row(self, table_model_object: Message) -> None:
        ...

    async def remove_row(self, table_model_object: Message) -> None:
        ...

    async def get_row(self, tabe_model_object: Message) -> Any:
        ...
