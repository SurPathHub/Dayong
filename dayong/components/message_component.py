"""
dayong.components.message_component
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Guild messaging tasks assigned to Dayong.
"""
import hikari
import tanjun

component = tanjun.Component()


@component.with_listener(hikari.MemberCreateEvent)
async def on_member_join(event: hikari.MemberCreateEvent) -> None:
    """Callback when a new member joins the server."""
    client = event.app.rest
    channels = await client.fetch_guild_channels(event.guild_id)
    for channel in channels:
        if "welcome" in channel.name:
            welcome_ch = await client.fetch_channel(channel.id)
            await welcome_ch.send("Greetings!")
            break


@tanjun.as_loader
def load_examples(client: tanjun.Client) -> None:
    client.add_component(component.copy())
