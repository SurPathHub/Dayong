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
from dayong.operations import ScheduledTaskDB

CLIENT = discord.Client()

config = DayongDynamicLoader.load()
sched = AsyncIOScheduler()


async def get_scheduled(table_model):
    db = ScheduledTaskDB()
    await db.connect(config)
    await db.create_table()
    result = await db.get_row(table_model)
    return result.one()


async def get_guild_channel(target_channel):
    channel: TextChannel
    for channel in CLIENT.guilds[0].channels:
        if target_channel == str(channel).strip():
            return channel


@sched.scheduled_job("interval", days=1)
async def get_devto_article():
    try:
        result = await get_scheduled(ScheduledTask(channel_name="", task_name="dev"))
    except NoResultFound:
        return

    if bool(result.run) is False:
        return

    content = await RESTClient().get_devto_article(sort_by_date=True)
    channel = await get_guild_channel(result.channel_name)

    if not isinstance(channel, TextChannel):
        raise TypeError

    logger.info(
        f"{get_devto_article.__name__} delivering content to: {result.channel_name}"
    )
    for content in content.content:
        print(content)
        await channel.send(content)
        await asyncio.sleep(60)


@sched.scheduled_job("interval", seconds=30)
async def get_medium_daily_digest():
    try:
        result = await get_scheduled(ScheduledTask(channel_name="", task_name="medium"))
    except NoResultFound:
        return

    if bool(result.run) is False:
        return

    email = config.email
    email_password = config.email_password
    channel = await get_guild_channel(result.channel_name)

    if email is None or email_password is None:
        await channel.send(
            "Can't retrieve content. Please check for missing email credentials 😕"
        )
        return

    client = EmailClient(config.imap_domain_name, email, email_password)
    content = await client.get_medium_daily_digest()

    for content in content.content:
        await channel.send(content)
        await asyncio.sleep(60)


@CLIENT.event
async def on_ready():
    sched.start()


CLIENT.run(DayongDynamicLoader.load().bot_token)
