"""
This module contains the exceptions that may disrupt the normal functioning
of Dayong and the exception handlers that are designed to handle some of them.
"""
from functools import wraps

from discord.ext.commands.errors import (  # type: ignore
    DiscordException,
    ExtensionAlreadyLoaded,
    ExtensionFailed,
    ExtensionNotFound,
    ExtensionNotLoaded,
    NoEntryPointError,
)


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


def ext_exception_handler(func):
    """Handle any raised `discord.ext.commands.errors.ExtensionError`
    subclass.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        async def tmp():
            failed_msg = "Failed to load {ext}. "
            try:
                await func(*args, **kwargs)
            except ExtensionNotFound as enf:
                return (
                    "Unable to find {ext}",
                    f"```python\n{enf}```",
                )

            except NoEntryPointError as npe:
                return (
                    failed_msg + "Check its `setup` entry point.",
                    f"```python\n{npe}```",
                )
            except ExtensionFailed as efe:
                return (
                    failed_msg + "Check its module or `setup` entry point.",
                    f"```python\n{efe}```",
                )
            except ExtensionAlreadyLoaded:
                pass
            except ExtensionNotLoaded:
                pass

        return tmp()

    return wrapper
