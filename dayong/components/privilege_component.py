"""
dayong.components.privilege_component
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Message commands and utilites for guild members with permissions.
"""
import time

import hikari
import tanjun
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from dayong.abc import DBProto
from dayong.models import AnonMessage

component = tanjun.Component()


@component.with_command
@tanjun.with_author_permission_check(128)
@tanjun.as_message_command("ping")
async def ping_command(ctx: tanjun.abc.Context) -> None:
    """Respond with pong and the time it takes for data to be transferred beetween
    Dayong and Discord's WebSocket server and REST API endpoints.

    Args:
        ctx (Context): Instantiated subclass of `tanjun.abc.Context`.
    """
    start_time = time.perf_counter()
    await ctx.respond(content="( ͡° ͜ʖ ͡°)")
    time_taken = (time.perf_counter() - start_time) * 1_000
    heartbeat_latency = (
        ctx.shards.heartbeat_latency * 1_000 if ctx.shards else float("NAN")
    )
    await ctx.edit_last_response(
        f"PONG\n - REST: {time_taken:.0f}ms\n - Gateway: {heartbeat_latency:.0f}ms"
    )


@component.with_command
@tanjun.with_author_permission_check(128)
@tanjun.with_argument("id")
@tanjun.with_parser
@tanjun.as_message_command("whois")
async def get_user_info(
    ctx: tanjun.abc.Context,
    str_id: str,
    database: DBProto = tanjun.injected(type=DBProto),
) -> None:
    """Reveal information on a user."

    Args:
        ctx (tanjun.abc.Context): Instance of `tanjun.abc.Context`.
        str_id (str): This can be a hash or the object or the ID of an
            existing user.
        database (DBProto): Interface for a database message table. This is a
            registered type dependency and is injected by the client.
    """
    await ctx.respond(content="Fetching user information, please wait...")
    try:
        if len(str_id) == 32 and str_id.isalnum():
            result = await database.get_row(
                AnonMessage(
                    message_id=str_id,
                    user_id="",
                    username="",
                    nickname="",
                    message="",
                )
            )
            info = result.first()
            if isinstance(info, (AnonMessage,)):
                await ctx.edit_last_response(
                    (
                        f"```ID: {info.user_id}\n"
                        f"Username: {info.username}\n"
                        f"Nickname: {info.nickname}```"
                    )
                )
            else:
                raise Exception(f"This ID does not exist: {str_id}")
        if str_id.isdigit():
            info = await ctx.rest.fetch_user(hikari.Snowflake(str_id))
            await ctx.edit_last_response(
                (
                    f"Username: {info.username}\n"
                    f"Avatar Hash: {info.avatar_hash}\n"
                    f"Avatar URL: {info.avatar_url}\n"
                    f"Default Avatar URL: {info.default_avatar_url}\n"
                    f"Discriminator: {info.discriminator}\n"
                    f"Flags: {info.flags}\n"
                    f"is Bot: {info.is_bot}\n"
                    f"is System: {info.is_system}\n"
                    f"Mention: {info.mention}```"
                )
            )
            return
        raise TypeError(
            f"This ID is invalid or of unknown type: {str_id}, length: {len(str_id)}"
        )
    except (SQLAlchemyError, TypeError, ValidationError, hikari.HikariError) as err:
        await ctx.edit_last_response(f"Something went wrong!\n`{err}`")


@tanjun.as_loader
def load_examples(client: tanjun.Client) -> None:
    """The loader for this component.

    Args:
        client (tanjun.Client): The client instance that will load this module.
    """
    client.add_component(component.copy())
