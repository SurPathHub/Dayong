"""
dayong.interfaces
~~~~~~~~~~~~~~~~~

Interfaces used within Dayong. We use protocol classes for structural subtyping.
"""
from typing import Optional, Protocol


class GuildConfig(Protocol):
    """Protocol class for guild configuration.

    Args:
        Protocol ([type]): The base class for Protocol classes.
    """

    @property
    def prefixes(self) -> list[str]:
        ...


class UserInfo(Protocol):
    """Protocol for user information.

    Args:
        Protocol ([type]): The base class for Protocol classes.
    """

    ...


class DatabaseProto(Protocol):
    """Protocol of a database connection.

    Args:
        Protocol ([type]): The base class for Protocol classes.
    """

    async def get_guild_info(self, guild_id: int) -> Optional[GuildConfig]:
        ...

    async def get_user_info(self, user_id: int) -> Optional[UserInfo]:
        ...

    async def remove_user(self, user_id: int) -> None:
        ...
