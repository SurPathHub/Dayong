"""
dayong.settings
~~~~~~~~~~~~~~~

Internal comments, flags, settings, and paths.
"""
import os
from pathlib import Path

from dotenv import load_dotenv
from rich.traceback import install

from dayong.configs import DayongConfig, DayongConfigLoader

# If the user is on a UNIX-like systemm this will replace the default asyncio event
# loop with one that uses libuv internally, uvloop.
if os.name != "nt":
    import uvloop

    uvloop.install()

# Parse the .env file and load the environment variables.
load_dotenv()

# Install traceback handler.
install(theme="monokai")

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
CONFIG_FILE = os.path.join(ROOT_DIR, "config.json")
CONFIG = DayongConfig(**DayongConfigLoader().__dict__)
