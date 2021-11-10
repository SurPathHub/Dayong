# type: ignore
# pylint: skip-file
import asyncio

import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import TextChannel
from loguru import logger
from sqlalchemy.exc import NoResultFound

from dayong.core.configs import DayongDynamicLoader
from dayong.exts.apis import RESTClient
from dayong.exts.emails import EmailClient
from dayong.models import ScheduledTask
from dayong.operations import DatabaseImpl

CONFIG = DayongDynamicLoader.load()
CLIENT = discord.Client()
rest = RESTClient()
email = None


@logger.catch
async def get_scheduled(table_model):
    db = DatabaseImpl()
    await db.connect(CONFIG)
    await db.create_table()
    return (await db.get_row(table_model, "task_name")).one()


@logger.catch
async def get_guild_channel(target_channel):
    channel: TextChannel
    for channel in CLIENT.guilds[0].channels:
        if target_channel == str(channel).strip():
            return channel


@logger.catch
async def check_email_cred():
    global email

    try:
        result = await get_scheduled(ScheduledTask(channel_name="", task_name="medium"))
    except NoResultFound:
        return

    email_host = CONFIG.imap_domain_name
    email_addr = CONFIG.email
    email_pass = CONFIG.email_password
    channel = await get_guild_channel(result.channel_name)

    if email_addr is None or email_pass is None:
        await channel.send(
            "Can't retrieve content on email subscription. Please provide your email "
            "credentials to do so 🔑"
        )
        return

    email = EmailClient(email_host, email_addr, email_pass)


@logger.catch
async def get_devto_article():
    task = get_devto_article.__name__

    try:
        result = await get_scheduled(ScheduledTask(channel_name="", task_name="dev"))
    except NoResultFound:
        logger.info(f"{task} is not scheduled to run")
        return

    if bool(result.run) is False:
        logger.info(f"{task} is not scheduled to run")
        return

    content = await rest.get_devto_article(sort_by_date=True)
    channel = await get_guild_channel(result.channel_name)

    if not isinstance(channel, TextChannel):
        raise TypeError

    logger.info(
        f"{get_devto_article.__name__} delivering content to: {result.channel_name}"
    )
    for content in content.content:
        await channel.send(content)
        await asyncio.sleep(30)


@logger.catch
async def get_medium_daily_digest():
    task = get_devto_article.__name__

    if email is None:
        logger.info(f"{task} cannot run. reason: missing email credentials")
        return

    try:
        result = await get_scheduled(ScheduledTask(channel_name="", task_name="medium"))
    except NoResultFound:
        logger.info(f"{task} is not scheduled to run")
        return

    if bool(result.run) is False:
        logger.info(f"{task} is not scheduled to run")
        return

    content = await email.get_medium_daily_digest()
    channel = await get_guild_channel(result.channel_name)

    logger.info(
        f"{get_medium_daily_digest.__name__} "
        "delivering content to: {result.channel_name}"
    )
    for content in content.content:
        await channel.send(content)
        await asyncio.sleep(30)


@CLIENT.event
async def on_ready():
    await check_email_cred()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(get_devto_article, "interval", days=1)
    scheduler.add_job(get_medium_daily_digest, "interval", days=1)
    scheduler.start()


CLIENT.run(CONFIG.bot_token)
