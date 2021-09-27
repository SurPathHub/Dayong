"""
dayong.components.slash_component
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Slash commands available for every guild member.
"""
from hashlib import md5
from random import shuffle

import hikari
import tanjun

from dayong.configs import DayongConfig
from dayong.impls import MessageDBImpl
from dayong.interfaces import MessageDBProto
from dayong.models import AnonMessage

component = tanjun.Component()


async def randomize_id(id: str) -> str:
    """Helper function to make IDs more unique and unexploitable.

    Args:
        id (str): The ID to randomize.

    Returns:
        str: A random-like ID.
    """
    shuffle(rand_id := list(md5(id.encode()).hexdigest()))
    return "".join(rand_id)


@component.with_slash_command
@tanjun.with_str_slash_option("message", "your anonymous message")
@tanjun.as_slash_command("anon", "Send anonymized messages", default_to_ephemeral=True)
async def anon_command(
    ctx: tanjun.abc.SlashContext,
    message: str,
    database: MessageDBProto = tanjun.injected(type=MessageDBImpl),
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
    try:
        if isinstance(ctx.member, hikari.InteractionMember) and isinstance(
            channel := await ctx.fetch_channel(), hikari.TextableChannel
        ):
            await database.create_table()
            message_id = await randomize_id(ctx.member.username)
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
    except Exception as err:
        await ctx.edit_initial_response(f"Something went wrong ❌\n`{err}`")


@tanjun.as_loader
def load_examples(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())
