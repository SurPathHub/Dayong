"""
This module contains the exceptions that may disrupt the normal functioning
of Dayong and the exception handlers that are designed to handle some of them.
"""
from functools import wraps

from discord.ext.commands.errors import DiscordException  # type: ignore


def exception_handler(func):
    """Raise and log generic exceptions."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DiscordException as clt_err:
            raise DiscordException(clt_err) from clt_err
        except Exception as gen_err:
            raise Exception(gen_err) from gen_err

    return wrapper
