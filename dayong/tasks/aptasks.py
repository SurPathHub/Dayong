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

db = DatabaseImpl()
rest = RESTClient()
email = None
info = ""


@logger.catch
async def get_scheduled(table_model):
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
        await asyncio.sleep(60)


@logger.catch
async def get_medium_daily_digest():
    task = get_devto_article.__name__
    notsched = f"{task} is not scheduled to run"
    xsession = f"{task} cannot run. reason: no session started.\n```{info}```"
    table_model = ScheduledTask(channel_name="", task_name="medium")

    try:
        result = await get_scheduled(table_model)
    except NoResultFound:
        logger.info(notsched)
        return

    if bool(result.run) is False:
        logger.info(notsched)
        return

    channel = await get_guild_channel(result.channel_name)

    if email is None:
        await channel.send(xsession)
        await del_schedule(table_model)
        return

    content = await email.get_medium_daily_digest()

    logger.info(
        f"{get_medium_daily_digest.__name__} "
        "delivering content to: {result.channel_name}"
    )
    for content in content.content:
        await channel.send(content)
        await asyncio.sleep(60)


@logger.catch
@CLIENT.event
async def on_ready():
    await check_email_cred()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(get_devto_article, "cron", day_of_week="mon-sun", hour=7)
    scheduler.add_job(get_medium_daily_digest, "cron", day_of_week="mon-sun", hour=7)
    scheduler.start()


CLIENT.run(CONFIG.bot_token)
