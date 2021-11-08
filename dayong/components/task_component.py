"""
dayong.components.task_components
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Scheduled tasks that run in the background.
"""
import hikari
import tanjun
from sqlalchemy.exc import NoResultFound

from dayong.abc import Database
from dayong.core.settings import CONTENT_PROVIDER
from dayong.models import ScheduledTask
from dayong.tasks.manager import TaskManagerMemory

component = tanjun.Component()
task_manager = TaskManagerMemory()

RESPONSE_INTVL = 30
RESPONSE_MESSG = {False: "Sorry, I got nothing for today 😔"}


async def start_task(context: tanjun.abc.Context, source: str, db: Database):
    """Start a scheduled task.

    Args:
        context (tanjun.abc.Context): Slash command specific context.
        source (str): Alias of the third-party content provider.
        db (Database): An instance of `dayong.operations.Database`.

    Raises:
        NotImplementedError: Raised if alias does not exist.
        ValueError: Raised if context failed to get the name of its channel.
        PermissionError: Raised if task is already scheduled.
    """
    if source not in CONTENT_PROVIDER.keys():
        raise NotImplementedError

    channel = context.get_channel()

    if channel is None:
        raise ValueError

    task_model = ScheduledTask(
        channel_name=channel.name if channel.name else "", task_name=source, run=True
    )

    try:
        await db.create_table()
        result = await db.get_row(task_model, "task_name")
        if bool(result.one().run) is False:
            raise PermissionError
        else:
            await db.update_row(task_model, "task_name")
            return
    except NoResultFound:
        await db.add_row(task_model)


async def stop_task(context: tanjun.abc.Context, source: str, db: Database):
    """Stop a scheduled task.

    Args:
        context (tanjun.abc.Context): Slash command specific context.
        source (str): Alias of the third-party content provider.
        db (Database): An instance of `dayong.operations.Database`.

    Raises:
        ValueError: Raised if context failed to get the name of its channel.
    """
    channel = context.get_channel()

    if channel is None:
        raise ValueError

    task_model = ScheduledTask(
        channel_name=channel.name if channel.name else "",
        task_name=source,
        run=False,
    )

    await db.remove_row(task_model, "task_name")


@component.with_command
@tanjun.with_author_permission_check(128)
@tanjun.with_str_slash_option("action", '"start" or "stop"')
@tanjun.with_str_slash_option("source", "e.g. medium or dev")
@tanjun.as_slash_command(
    "content", "fetch content on email subscription, from a service, or API"
)
async def share_content(
    ctx: tanjun.abc.SlashContext,
    source: str,
    action: str,
    db: Database = tanjun.injected(type=Database),
) -> None:
    """Fetch content on email subscription, from a service, or API.

    An email account is required for getting content on email subscription. Special
    keys may be required for using services and/or APIs.

    Args:
        ctx (tanjun.abc.Context): Interface of a context.
        source (str): Alias of the third-party content provider.
        action (str): Start or stop the content retrival task.
        db (Database): An instance of `dayong.operations.Database`.
            Defaults to tanjun.injected(type=Database).
    """
    action = action.lower()

    if action == "start":
        try:
            await start_task(ctx, source, db)
            await ctx.respond(
                f"Will comeback here to deliver content from `{source}` 📰"
            )
        except PermissionError:
            await ctx.respond("Already doing that 👌")
        except NotImplementedError:
            description = [f"`{provider}`" for provider in CONTENT_PROVIDER]
            await ctx.respond(f"Oops! `{source}` isn't available.")
            await ctx.respond(
                hikari.Embed(
                    title="Supported content providers:",
                    description="\n".join(description),
                )
            )
            return
    elif action == "stop":
        try:
            await stop_task(ctx, source, db)
            await ctx.respond(f"Stopped content delivery for `{source}`")
        except NoResultFound:
            await ctx.respond("That task isn't running 🤔")
    else:
        await ctx.respond(
            f"This doesn't seem to be a valid command argument: `{action}` 🤔"
        )


@tanjun.as_loader
def load_examples(client: tanjun.abc.Client) -> None:
    """The loader for this component.

    Args:
        client (tanjun.Client): The client instance that will load this module.
    """
    client.add_component(component.copy())
