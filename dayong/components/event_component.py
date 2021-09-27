"""
dayong.components.event_component
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Organization of events and event listeners.
"""
from typing import Optional

import hikari
import tanjun

from dayong.configs import DayongConfig

component = tanjun.Component()


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
        for info in range(len(embeddings["greetings_field"])):
            inner_dict = embeddings["greetings_field"][info]
            embed.add_field(
                name=inner_dict["name"],
                value=inner_dict["value"],
                inline=True,
            )

        await wc_channel.send(embed)


@tanjun.as_loader
def load_examples(client: tanjun.Client) -> None:
    client.add_component(component.copy())
