"""
dayong.impls
~~~~~~~~~~~~

Implementaion of interfaces and the logic for injecting them. We want to separate the
code here from the interfaces module for maintainability.

NOTE: Explicitly declare that a class implements a protocol.
"""
from typing import Any, Optional

# import sqlmodel
from tanjun import injected

from dayong.configs import DayongConfig
from dayong.interfaces import DatabaseProto, GuildConfig, UserInfo


async def connect_to_database(*args: Any, **kwargs: Any) -> Any:
    raise NotImplementedError


class DatabaseImpl(DatabaseProto):
    def __init__(self, connection: Any) -> None:
        self._conn = connection

    async def get_guild_info(self, guild_id: int) -> Optional[GuildConfig]:
        raise NotImplementedError

    async def get_user_info(self, user_id: int) -> Optional[UserInfo]:
        raise NotImplementedError

    async def remove_user(self, user_id: int) -> None:
        raise NotImplementedError

    @classmethod
    async def connect(cls, config: DayongConfig = injected(type=DayongConfig)):
        return cls(await connect_to_database())
