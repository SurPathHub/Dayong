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
from dayong.exts.apis import RESTClient
from dayong.exts.emails import EmailClient
from dayong.settings import CONTENT_PROVIDER
from dayong.tasks.manager import TaskManager

component = tanjun.Component()
task_manager = TaskManager()
ext_instance: dict[str, Any] = {}

RESPONSE_INTVL = 60
RESPONSE_MESSG = {False: "Sorry, I got nothing for today 😔"}


async def _set_response_intvl() -> int:
    """Set interval according to number of tasks running which should prevent
    rate-limiting.

    Returns:
        int: RESPONSE_INTVL
    """
    tasks = len(ext_instance)
    if tasks >= 2:
        return RESPONSE_INTVL + tasks
    return RESPONSE_INTVL


async def _set_ext_instance(ext_class: str, ext_class_instance: Any, *args: Any) -> Any:
    """Save and track instances which may be used by other scheduled tasks.

    Args:
        ext_class (str): The name of the class.
        ext_class_instance (Any): Any instantiable class.

    Returns:
        Any: The same instance passed as an argument to this function.
    """
    if ext_class not in ext_instance:
        if args:
            instance = ext_class_instance(*args)
        else:
            instance = ext_class_instance()
        ext_instance[ext_class] = instance
    else:
        instance = ext_instance[ext_class]

    return instance


async def _set_ext_loop(
    ctx: tanjun.abc.SlashContext, content: Union[list[Any], Any], response_intvl: int
) -> None:
    """Respond with retrieved content.

    Args:
        ctx (tanjun.abc.SlashContext): Slash command specific context.
        content (Union[list[Any], Any]): The fetched content.
        response_intvl (int): Interval between each response.
    """
    if content:
        for article in content:
            await ctx.respond(article)
            await asyncio.sleep(response_intvl)
    else:
        await ctx.respond(f"dev.to: {RESPONSE_MESSG[False]}")


async def _devto_article(ctx: tanjun.abc.SlashContext, *args: Any) -> NoReturn:
    """Async wrapper for `dayong.tasks.get_devto_article()`

    This coroutine is tasked to retrieve dev.to content on REST API endpoints and
    deliver fetched content every `RESPONSE_INTVL` seconds.

    Args:
        ctx (tanjun.abc.SlashContext): Slash command specific context.
    """
    response_intvl = await _set_response_intvl()
    client = await _set_ext_instance(RESTClient.__name__, RESTClient)
    assert isinstance(client, RESTClient)

    while True:
        articles = await client.get_devto_article()
        await _set_ext_loop(ctx, articles.content, response_intvl)


async def _medium_daily_digest(
    ctx: tanjun.abc.SlashContext, config: DayongConfig
) -> Union[NoReturn, None]:
    """Async wrapper for `dayong.tasks.get_medium_daily_digest()`.

    This coroutine is tasked to retrieve medium content on email subscription and
    deliver fetched content every `RESPONSE_INTVL` seconds.

    Args:
        ctx (tanjun.abc.SlashContext): Slash command specific context.
        config (DayongConfig): Instance of `dayong.configs.DayongConfig`.
    """
    response_intvl = await _set_response_intvl()
    email = config.email
    email_password = config.email_password

    if email is None or email_password is None:
        await ctx.respond(
            "Can't retrieve content. Please check for missing email credentials 😕"
        )
        return

    client = await _set_ext_instance(
        EmailClient.__name__,
        EmailClient,
        config.imap_domain_name,
        config.email,
        email_password,
    )
    assert isinstance(client, EmailClient)

    while True:
        articles = await client.get_medium_daily_digest()
        content = articles.content
        await _set_ext_loop(ctx, content, response_intvl)


async def assign_task(
    source: str, interval: Union[int, float]
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
    interval = interval if interval >= 86400.0 else 86400.0
    task_cstr = {
        "medium": (
            _medium_daily_digest.__name__,
            _medium_daily_digest,
            interval,
        ),
        "dev": (
            _devto_article.__name__,
            _devto_article,
            interval,
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
    "the interval between each content delivery. minimum of 86400.0 (24 hours)",
    converters=float,
)
@tanjun.with_str_slash_option("source", "e.g. medium or dev")
@tanjun.as_slash_command(
    "content", "fetch content on email subscription, from a microservice, or API"
)
async def share_content(
    ctx: tanjun.abc.Context,
    source: str,
    interval: float,
    action: str,
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
        description = [f"`{provider}`" for provider in CONTENT_PROVIDER]
        await ctx.respond(f"Oops! `{source}` isn't available.")
        await ctx.respond(
            hikari.Embed(
                title="Supported content providers:",
                description="\n".join(description),
            )
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
            await ctx.respond(
                f"I'll comeback here to deliver content from `{source}` 📰"
            )
        except PermissionError:
            await ctx.respond("I'm already doing that 👌")
    elif action == "stop":
        task_manager.stop_task(task_nm)
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
