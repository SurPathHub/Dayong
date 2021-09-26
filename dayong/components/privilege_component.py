"""
dayong.components.privilege_component
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Message commands and utilites for guild members with permissions.
"""
import time

import tanjun

component = tanjun.Component()


@component.with_command
@tanjun.with_author_permission_check(32)
@tanjun.as_message_command("ping")
async def ping_command(ctx: tanjun.abc.Context) -> None:
    """Respond with pong and the time it takes for data to be transferred beetween
    Dayong and Discord's WebSocket server and REST API endpoints.

    Args:
        ctx (Context): Instantiated subclass of `tanjun.abc.Context`.
    """
    start_time = time.perf_counter()
    await ctx.respond(content="( ͡° ͜ʖ ͡°)")
    time_taken = (time.perf_counter() - start_time) * 1_000
    heartbeat_latency = (
        ctx.shards.heartbeat_latency * 1_000 if ctx.shards else float("NAN")
    )
    await ctx.edit_last_response(
        f"PONG\n - REST: {time_taken:.0f}ms\n - Gateway: {heartbeat_latency:.0f}ms"
    )


@tanjun.as_loader
def load_examples(client: tanjun.Client) -> None:
    client.add_component(component.copy())
