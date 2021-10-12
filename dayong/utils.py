"""
dayong.utils
~~~~~~~~~~~~
This module provides useful functions that facilitate some of Dayong's routine
operations.
"""
import asyncio
import functools
from typing import Any, Awaitable, Callable

SUPPORTED_DB = ("postgres://",)


def format_db_url(database_url: str) -> str:
    """Format the default database URL to support async requests/transactions.
    One case this is useful is when the hosting provider automatically provisions the
    database and changing the database URL isn't simple.
    Args:
        database_url (str): The default url of a supported database.
    Returns:
        str: A unique sequence of characters that identifies the database.
    """
    db_scheme = next(
        se_scheme if se_scheme in database_url else "" for se_scheme in SUPPORTED_DB
    )

    if not db_scheme:
        return database_url

    if db_scheme == "postgres://":
        db_name = "postgresql://"
    else:
        db_name = db_scheme

    return database_url.replace(
        db_scheme, f"""{db_name.replace("://", "+asyncpg://")}"""
    )


def run_in_executor(blocking_fn: Callable[..., Any]) -> Callable[..., Awaitable[Any]]:
    """Decorator for executing blocking code asynchronously.
    Args:
        blocking_fn (Callable[..., Any]): A blocking function or method.
    Returns:
        Callable[..., Awaitable[Any]]: An awaitable object.
    """

    @functools.wraps(blocking_fn)
    async def inner(*args: Any, **kwargs: Any):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: blocking_fn(*args, **kwargs))

    return inner


def validate_cfg(config: dict[str, Any], valid: dict[str, Any]) -> None:
    """Check configuration accuracy.
    Args:
        config (dict[str, Any]): Parsed JSON file.
        valid (dict[str, Any]): Representation of a valid configuration.
    Raises:
        KeyError: Raised if the key in the config is invalid.
        TypeError: If a config value is an incompatible data type.
    """
    for key, value in list(config.items()):
        if isinstance(value, dict):
            try:
                validate_cfg(config[key], valid[key])
            except KeyError as key_err:
                raise KeyError(f'key "{key}" is not a valid configuration') from key_err
        elif not isinstance(value, valid[key]):
            raise TypeError(
                f'"{value}" in key {key} is the incorrect type'
                f" {type(value)}, must be {valid[key]}",
            )


if __name__ == "__main__":
    pass
