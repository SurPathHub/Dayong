# type: ignore
# pylint: skip-file
import asyncio
import time

import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import TextChannel
from loguru import logger
from pragmail.exceptions import IMAP4Error
from sqlalchemy.exc import NoResultFound

from dayong.core.configs import DayongDynamicLoader
from dayong.exts.apis import RESTClient
from dayong.exts.emails import EmailClient
from dayong.models import ScheduledTask
from dayong.operations import DatabaseImpl
from dayong.tasks.manager import AioTaskManager

CONFIG = DayongDynamicLoader.load()
CLIENT = discord.Client()

db = DatabaseImpl()
rest = RESTClient()
tm = AioTaskManager()
email = None
info = ""
job_ran = False


async def signal_run() -> None:
    global job_ran

    job_ran = True


async def check_rate() -> None:
    global job_ran

    if job_ran is True:
        # Intentionally blocking
        time.sleep(5)
        job_ran = False


@logger.catch
async def get_scheduled(table_model):
    await db.connect(CONFIG)
    await db.create_table()
    try:
        return (await db.get_row(table_model, "task_name")).one()
    except NoResultFound:
        return None


@logger.catch
async def get_guild_channel(target_channel):
    for channel in CLIENT.guilds[0].channels:
        if target_channel == str(channel).strip():
            return channel


@logger.catch
async def del_schedule(table_model):
    try:
        await db.connect(CONFIG)
        await db.remove_row(table_model, "task_name")
    except NoResultFound:
        logger.info(f"{repr(table_model)} not found")


@logger.catch
async def check_email_cred():
    global email, info

    email_host = CONFIG.imap_domain_name
    email_addr = CONFIG.email
    email_pass = CONFIG.email_password

    if email_addr is None or email_pass is None:
        info = (
            "Can't retrieve content on email subscription. To do so, please "
            "provide your email credentials and redeploy the bot."
        )
        logger.info(info)
        return

    email = EmailClient(email_host, email_addr, email_pass)


@logger.catch
async def send_content(channel, content):
    for content in content.content:
        await check_rate()
        await channel.send(content)
        await signal_run()
        await asyncio.sleep(60)


@logger.catch
async def get_devto_article():
    task = get_devto_article.__name__

    result = await get_scheduled(ScheduledTask(channel_name="", task_name="dev"))

    if not result or bool(result.run) is False:
        logger.info(f"{task} is not scheduled to run")
        return

    content = await rest.get_devto_article()
    channel = await get_guild_channel(result.channel_name)

    if not isinstance(channel, TextChannel):
        raise TypeError(f"channel is not a TextChannel: {channel}")

    logger.info(
        f"{get_devto_article.__name__} delivering content to: {result.channel_name}"
    )

    await tm.stop_task(task)
    await tm.start_task(send_content, task, 0, channel, content)


@logger.catch
async def get_medium_daily_digest():
    global email

    task = get_medium_daily_digest.__name__
    notsched = f"{task} is not scheduled to run"
    xsession = f"{task} cannot run. reason: no session started.\n```{info}```"
    table_model = ScheduledTask(channel_name="", task_name="medium")

    result = await get_scheduled(table_model)

    if not result:
        logger.info(f"{task} is not scheduled to run")
        return

    if bool(result.run) is False:
        logger.info(notsched)
        return

    channel = await get_guild_channel(result.channel_name)

    if not isinstance(channel, TextChannel):
        raise TypeError(f"channel is not a TextChannel: {channel}")

    if email is None:
        await channel.send(xsession)
        await del_schedule(table_model)
        return

    try:
        content = await email.get_medium_daily_digest()
    except IMAP4Error:
        email = EmailClient(
            CONFIG.imap_domain_name, CONFIG.email, CONFIG.email_password
        )
        content = await email.get_medium_daily_digest()

    logger.info(
        f"{get_medium_daily_digest.__name__} "
        "delivering content to: {result.channel_name}"
    )

    await tm.stop_task(task)
    await tm.start_task(send_content, task, 0, channel, content)


@logger.catch
@CLIENT.event
async def on_ready():
    await check_email_cred()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(get_devto_article, "interval", hours=24)
    scheduler.add_job(get_medium_daily_digest, "interval", hours=24)
    scheduler.start()


CLIENT.run(CONFIG.bot_token)
