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
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from dayong.configs import DayongConfig
=======

from dayong.configs import DayongConfig
from dayong.impls import MessageDBImpl
>>>>>>> a34eab6... feat: add functional slash command
from dayong.interfaces import MessageDBProto
from dayong.models import AnonMessage

component = tanjun.Component()


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
    return "".join(rand_id)


@component.with_slash_command
@tanjun.with_str_slash_option("message", "your anonymous message")
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
async def anon_command(
    ctx: tanjun.abc.SlashContext,
    message: str,
    database: MessageDBProto = tanjun.injected(type=MessageDBImpl),
    config: DayongConfig = tanjun.injected(type=DayongConfig),
) -> None:
    await ctx.defer()
    if isinstance(ctx.member, hikari.InteractionMember) and isinstance(
        channel := await ctx.fetch_channel(), hikari.TextableChannel
    ):
        await database.create_table()
        message_id = await generate_random_id(ctx.member.username)
        await database.add_row(
            AnonMessage(
                message_id=message_id,
                user_id=ctx.member.id,
                username=ctx.member.username,
                nickname=ctx.member.nickname
                if ctx.member.nickname
                else ctx.member.username,
                message=message,
            )
        )
        embeddings = config.embeddings["anonymous_message"]
        await channel.send(
            embed=hikari.Embed(
                title=f"""{embeddings["title"]} • {message_id}""",
                description=f"`{message}`",
                color=embeddings["color"],
            )
        )
        await ctx.edit_initial_response("Message sent ✅")
        return
    await ctx.edit_initial_response("Something went wrong ❌")
>>>>>>> a34eab6... feat: add functional slash command


@tanjun.as_loader
def load_examples(client: tanjun.abc.Client) -> None:
<<<<<<< HEAD
    """The loader for this component.

    Args:
        client (tanjun.Client): The client instance that will load this module.
    """
=======
>>>>>>> a34eab6... feat: add functional slash command
    client.add_component(component.copy())
