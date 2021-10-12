"""
dayong.components.task_components
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Scheduled tasks that run in the background.
"""
import asyncio
from typing import Any, Callable, Coroutine, NoReturn, Union

import hikari
import tanjun

from dayong.configs import DayongConfig
from dayong.exts.emails import EmailClient
from dayong.tasks.manager import TaskManager

component = tanjun.Component()
task_manager = TaskManager()
ext_instance: dict[str, Any] = {}

# Available 3rd party content providers.
CONTENT_PROVIDER = {
    "medium",
}


async def _medium_daily_digest(
    ctx: tanjun.abc.SlashContext, config: DayongConfig
) -> NoReturn:
    """Extend `medium_daily_digest` and execute
    `dayong.tasks.get_medium_daily_digest` as a coro.

    This coroutine is tasked to retrieve medium content on email subscription and
    deliver fetched content every 30 seconds. 30 seconds is set to avoid rate-limiting.

    Args:
        ctx (tanjun.abc.SlashContext): Slash command specific context.
        host (str): The URL of the email provider's IMAP server.
    """
    ext_class = EmailClient.__name__

    if ext_class not in ext_instance:
        email = EmailClient.client(
            config.imap_host, config.email, config.email_password
        )
        ext_instance[ext_class] = email
    else:
        email: EmailClient = ext_instance[ext_class]

    while True:
        articles = await email.get_medium_daily_digest()
        if articles:
            for article in articles:
                await ctx.respond(article)
                await asyncio.sleep(30)
        else:
            await ctx.respond("Sorry, I got nothing for today 😔")


async def assign_task(
    source: str,
    interval: Union[int, float],
) -> tuple[str, Callable[..., Coroutine[Any, Any, Any]], float]:
    """Get the coroutine for the given task specified by source.

    Args:
        source (str): The name of the task to be assigned.

    Raises:
        NotImplementedError: Raised if the task or feature has not been implemented.
        ValueError: Raised if the specified task does not exist.

    Returns:
        tuple[str, Callable[..., Coroutine[Any, Any, Any]]]: A tuple containing the
            task name and the callable for the task.
    """
    task_cstr = {
        "medium": (
            _medium_daily_digest.__name__,
            _medium_daily_digest,
            interval if interval >= 86400.0 else 86400.0,
        ),
    }

    try:
        task_nm, task_fn, interval = task_cstr[source]
    except KeyError as key_err:
        raise NotImplementedError from key_err

    return task_nm, task_fn, interval


@component.with_command
@tanjun.with_author_permission_check(128)
@tanjun.with_str_slash_option("action", '"start" or "stop"')
@tanjun.with_str_slash_option(
    "interval",
    (
        "wait time in seconds until next content delivery. "
        "email sub-based content should be >= 86400.0 (24H)"
    ),
    converters=float,
)
@tanjun.with_str_slash_option("source", "e.g. medium or dev.to")
@tanjun.as_slash_command(
    "content", "fetch content on email subscription, from a microservice, or API"
)
async def share_content(
    ctx: tanjun.abc.Context,
    source: str,
    action: str,
    interval: float,
    config: DayongConfig = tanjun.injected(type=DayongConfig),
) -> None:
    """Fetch content on email subscription, from a microservice, or API.

    An email account is required for getting content on email subscription. Special
    keys may be required for using microservices and/or APIs.

    Args:
        ctx (tanjun.abc.Context): Interface of a context.
        action (str): Start or stop the content retrival task.
        config (DayongConfig, optional): An instance of `dayong.configs.DayongConfig`.
            Defaults to tanjun.injected(type=DayongConfig).
    """
    action = action.lower()
    try:
        task_nm, task_fn, interval = await assign_task(source, interval)
    except NotImplementedError:
<<<<<<< HEAD
        description = [f"`{provider}`" for provider in CONTENT_PROVIDER]
        await ctx.respond(f"Oops! `{source}` isn't available.")
        await ctx.respond(
            hikari.Embed(
                title="Supported content providers:",
                description="\n".join(description),
            )
=======
        await ctx.respond(
            f"Oops! `{source}` isn't available yet. "
            "Request it to be added by posting an issue here: "
            "https://github.com/SurPathHub/Dayong/issues"
>>>>>>> c29273c... fix: handle NotImplementedError
        )
        return

    if action == "start":
        try:
            await task_manager.start_task(
                task_fn,
                task_nm,
                interval,
                ctx,
                config,
            )
            await ctx.respond("I'll comeback here to deliver articles and blog posts 📰")
        except RuntimeError:
            await ctx.respond("I'm already doing that 👌")
    elif action == "stop":
        task_manager.get_task(task_nm).cancel()
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
