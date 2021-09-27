"""
dayong.components.event_component
<<<<<<< HEAD
<<<<<<< HEAD
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Organization of events and event listeners.
"""
from typing import Optional, Sequence
=======
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
=======
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
>>>>>>> a34eab6... feat: add functional slash command

Organization of events and event listeners.
"""
from typing import Optional
>>>>>>> 0cf3e58... chore: use more aprop component names

import hikari
import tanjun

<<<<<<< HEAD
<<<<<<< HEAD
from dayong.configs import DayongConfig
=======
from dayong.settings import CONFIG
>>>>>>> 0cf3e58... chore: use more aprop component names
=======
from dayong.configs import DayongConfig
>>>>>>> a34eab6... feat: add functional slash command

component = tanjun.Component()


<<<<<<< HEAD
async def get_channel(
    channels: Sequence[hikari.GuildChannel],
    channel_name: str,
) -> tuple[str, Optional[hikari.GuildChannel]]:
    """Search for channels use the first channel that matches the specified channel
    name.

    Args:
        channels (Sequence[hikari.GuildChannel]): An instance of `hikari.GuildChannel`.
        channel_name (str): The name of the target channel.

    Returns:
        list[str]: A list of channel names that matched the specified channel name.
    """
    target_channel = ("", None)

    for channel in channels:
        if channel.name is not None and channel_name in channel.name:
            target_channel = (channel.name, channel)
            break

    return target_channel


@component.with_listener(hikari.MemberCreateEvent)
async def greet_new_member(
    event: hikari.MemberCreateEvent,
    config: DayongConfig = tanjun.injected(type=DayongConfig),
) -> None:
    """Welcome new guild members. This will send a message greetings to a welcome
    channel.

    Args:
        event (hikari.MemberCreateEvent): Instance of `hikari.MemberCreateEvent`. This
            is a registered type dependency and is injected by the client.
        config (DayongConfig, optional): An instance of `dayong.configs.DayongConfig`.
            This is registered type dependency and is injected by the client. Defaults
            to tanjun.injected(type=DayongConfig).
    """
    embeddings = config.embeddings["new_member_greetings"]
    channels = await event.app.rest.fetch_guild_channels(event.guild_id)
    wc_channel, wc_object = await get_channel(channels, "welcome")

    if wc_channel and wc_object:
        wc_txtable = await event.app.rest.fetch_channel(wc_object.id)
    else:
        wc_txtable = None

    if isinstance(wc_txtable, hikari.TextableChannel) and isinstance(embeddings, dict):
        embed = hikari.Embed(
            description=embeddings["description"].format(
                hikari.OwnGuild.name,
                event.member.id,
                embeddings["readme_channel_id"],
            ),
            color=embeddings["color"],
        )

=======
@component.with_listener(hikari.MemberCreateEvent)
async def greet_new_member(
    event: hikari.MemberCreateEvent,
    config: DayongConfig = tanjun.injected(type=DayongConfig),
) -> None:
    """Welcome new guild members.

    This will dynamically search for welcome channels, sort the channels by name length
    and send a greeting to the channel with the shortest name.

    Args:
        event (hikari.MemberCreateEvent): Instance of `hikari.MemberCreateEvent`. This
            is a registered type dependency and is injected by the client.
    """
    embeddings = config.embeddings["new_member_greetings"]
    wc_channel: Optional[hikari.TextableChannel] = None
    channels = await event.app.rest.fetch_guild_channels(event.guild_id)

    if isinstance(channels, list):
        channels.sort(key=len)

    for channel in channels:
        if "welcome" in str(channel.name):
            wc_channel = (
                wch
                if isinstance(
                    (wch := await event.app.rest.fetch_channel(channel.id)),
                    hikari.TextableChannel,
                )
                else None
            )
            break

    if wc_channel:
        embed = hikari.Embed(
            description=embeddings["description"].format(
                hikari.OwnGuild.name,
                event.member.id,
                embeddings["readme_channel_id"],
            ),
            color=embeddings["color"],
        )
>>>>>>> 0cf3e58... chore: use more aprop component names
        for info in range(len(embeddings["greetings_field"])):
            inner_dict = embeddings["greetings_field"][info]
            embed.add_field(
                name=inner_dict["name"],
                value=inner_dict["value"],
                inline=True,
            )

<<<<<<< HEAD
        await wc_txtable.send(embed)
=======
        await wc_channel.send(embed)
>>>>>>> 0cf3e58... chore: use more aprop component names


@tanjun.as_loader
def load_examples(client: tanjun.Client) -> None:
<<<<<<< HEAD
    """The loader for this component.

    Args:
        client (tanjun.Client): The client instance that will load this module.
    """
=======
>>>>>>> 0cf3e58... chore: use more aprop component names
    client.add_component(component.copy())
