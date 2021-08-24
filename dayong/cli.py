"""
Dayong's user-friendly command-line interface.
"""
import argparse
import os

from dayong.bot import BASE_DIR, Setup


class SetupCLI(Setup):
    """A subclass of `dayong.bot.Setup`. This is only for external use."""


def display_banner() -> None:
    """Open banner file and display its contents."""
    bpath = os.path.join(BASE_DIR, "banner.txt")
    with open(bpath, "r", encoding="utf-8") as banner:
        print(banner.read())


def command_line() -> argparse.Namespace:
    """Parse command-line options, arguments and sub-commands."""
    parser = argparse.ArgumentParser(
        description=(
            "For more information, please visit the project repository at "
            "https://github.com/SurPathHub/Dayong."
        )
    )
    parser.add_argument(
        "--use_config",
        default="False",
        type=bool,
        help="Use the config.json to configure the bot (default: False)",
    )

    return parser.parse_args()


if __name__ == "__main__":
    pass
