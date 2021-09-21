"""
dayong.settings
~~~~~~~~~~~~~~~

Internal comments, flags, settings, and paths.
"""
import os
from pathlib import Path

from dotenv import load_dotenv
from rich.traceback import install

# Parse the .env file and load the environment variables.
load_dotenv()

# Install traceback handler.
# TODO: report bug in `rich.traceback.Traceback`; extract()'s traceback
# parameter is missing a default value. Include concern over annotations.
install(theme="monokai")

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
CONFIG_FILE = os.path.join(ROOT_DIR, "config.json")
