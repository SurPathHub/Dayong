"""
dayong.components.slash_component
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Slash commands available for every guild member.
"""
from hashlib import md5
from random import shuffle

import hikari
import tanjun
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> f22a397... refactor: apply linter on components
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from dayong.configs import DayongConfig
=======

from dayong.configs import DayongConfig
<<<<<<< HEAD
from dayong.impls import MessageDBImpl
>>>>>>> a34eab6... feat: add functional slash command
=======
>>>>>>> fd9070d... refactor: apply pyright
from dayong.interfaces import MessageDBProto
from dayong.models import AnonMessage

component = tanjun.Component()


<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
async def randomize_id(str_id: str) -> str:
    """Helper function to make IDs more unique and unexploitable.

    Args:
        str_id (str): The ID to randomize.

    Returns:
        str: A random-like ID.
    """
    shuffle(rand_id := list(md5(str_id.encode()).hexdigest()))
=======
async def generate_random_id(string: str) -> str:
    shuffle(rand_id := list(md5(string.encode()).hexdigest()))
>>>>>>> a34eab6... feat: add functional slash command
=======
async def randomize_id(id: str) -> str:
=======
async def randomize_id(str_id: str) -> str:
>>>>>>> f22a397... refactor: apply linter on components
    """Helper function to make IDs more unique and unexploitable.

    Args:
        str_id (str): The ID to randomize.

    Returns:
        str: A random-like ID.
    """
<<<<<<< HEAD
    shuffle(rand_id := list(md5(id.encode()).hexdigest()))
>>>>>>> e6bbba2... docs: add function and method docstring
=======
    shuffle(rand_id := list(md5(str_id.encode()).hexdigest()))
>>>>>>> f22a397... refactor: apply linter on components
    return "".join(rand_id)


@component.with_slash_command
@tanjun.with_str_slash_option("message", "your anonymous message")
<<<<<<< HEAD
<<<<<<< HEAD
@tanjun.as_slash_command("anon", "Send anonymized messages", default_to_ephemeral=True)
async def anon_command(
    ctx: tanjun.abc.SlashContext,
    message: str,
    database: MessageDBProto = tanjun.injected(type=MessageDBProto),
    config: DayongConfig = tanjun.injected(type=DayongConfig),
) -> None:
    """Allow a user or server member to send anonymous messages on Discord.

    Args:
        ctx (tanjun.abc.SlashContext): Interface of a context.
        message (str): The message to anonymize.
        database (MessageDBProto): Interface for a database message table. This is a
            registered type dependency and is injected by the client.
        config (DayongConfig): An instance of `dayong.configs.DayongConfig`. Also a
            registered type dependency and is injected by the client.
    """
    await ctx.defer()
    channel = await ctx.fetch_channel()
    try:
        if isinstance(ctx.member, hikari.InteractionMember):
            await database.create_table()
            message_id = await randomize_id(ctx.member.username)
            await database.add_row(
                AnonMessage(
                    message_id=message_id,
                    user_id=str(ctx.member.id),
                    username=ctx.member.username,
                    nickname=ctx.member.nickname
                    if ctx.member.nickname
                    else ctx.member.username,
                    message=message,
                )
            )
            embeddings = config.embeddings["anonymous_message"]
            if isinstance(embeddings, dict):
                await channel.send(
                    embed=hikari.Embed(
                        title=f"""{embeddings["title"]} • {message_id}""",
                        description=f"`{message}`",
                        color=embeddings["color"],
                    )
                )
            await ctx.edit_initial_response("Message sent ✅")
    except (SQLAlchemyError, ValidationError, hikari.HikariError) as err:
        await ctx.edit_initial_response(f"Something went wrong ❌\n`{err}`")
=======
@tanjun.as_slash_command("anon", "Send anonymized message", default_to_ephemeral=True)
=======
@tanjun.as_slash_command("anon", "Send anonymized messages", default_to_ephemeral=True)
>>>>>>> 94a35c7... docs: update docs
async def anon_command(
    ctx: tanjun.abc.SlashContext,
    message: str,
    database: MessageDBProto = tanjun.injected(type=MessageDBProto),
    config: DayongConfig = tanjun.injected(type=DayongConfig),
) -> None:
    """Allow a user or server member to send anonymous messages on Discord.

    Args:
        ctx (tanjun.abc.SlashContext): Interface of a context.
        message (str): The message to anonymize.
        database (MessageDBProto): Interface for a database message table. This is a
            registered type dependency and is injected by the client.
        config (DayongConfig): An instance of `dayong.configs.DayongConfig`. Also a
            registered type dependency and is injected by the client.
    """
    await ctx.defer()
    channel = await ctx.fetch_channel()
    try:
        if isinstance(ctx.member, hikari.InteractionMember):
            await database.create_table()
            message_id = await randomize_id(ctx.member.username)
            await database.add_row(
                AnonMessage(
                    message_id=message_id,
                    user_id=str(ctx.member.id),
                    username=ctx.member.username,
                    nickname=ctx.member.nickname
                    if ctx.member.nickname
                    else ctx.member.username,
                    message=message,
                )
            )
            embeddings = config.embeddings["anonymous_message"]
            if isinstance(embeddings, dict):
                await channel.send(
                    embed=hikari.Embed(
                        title=f"""{embeddings["title"]} • {message_id}""",
                        description=f"`{message}`",
                        color=embeddings["color"],
                    )
                )
<<<<<<< HEAD
            )
<<<<<<< HEAD
        )
        await ctx.edit_initial_response("Message sent ✅")
        return
    await ctx.edit_initial_response("Something went wrong ❌")
>>>>>>> a34eab6... feat: add functional slash command
=======
=======
>>>>>>> fa179fc... refactor: improve typing parity
            await ctx.edit_initial_response("Message sent ✅")
    except (SQLAlchemyError, ValidationError, hikari.HikariError) as err:
        await ctx.edit_initial_response(f"Something went wrong ❌\n`{err}`")
>>>>>>> 0686459... docs: update docstrings


@tanjun.as_loader
def load_examples(client: tanjun.abc.Client) -> None:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    """The loader for this component.
=======
    """The loader this component.
>>>>>>> f22a397... refactor: apply linter on components
=======
    """The loader for this component.
>>>>>>> 7b2c057... docs: fix wording

    Args:
        client (tanjun.Client): The client instance that will load this module.
    """
<<<<<<< HEAD
=======
>>>>>>> a34eab6... feat: add functional slash command
=======
>>>>>>> f22a397... refactor: apply linter on components
    client.add_component(component.copy())
