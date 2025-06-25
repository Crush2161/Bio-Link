import os
import re
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
env_path = Path('.') / '.env'
if env_path.exists():
    load_dotenv()

# Try to get from environment variables (Heroku Config Vars)
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH") 
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")

# If env vars are not set, try to load from env_config.json
if not all([API_ID, API_HASH, BOT_TOKEN, MONGO_URI]):
    try:
        with open("env_config.json", "r") as f:
            config = json.load(f)
            API_ID = API_ID or config.get("API_ID")
            API_HASH = API_HASH or config.get("API_HASH")
            BOT_TOKEN = BOT_TOKEN or config.get("BOT_TOKEN")
            MONGO_URI = MONGO_URI or config.get("MONGO_URI")
    except FileNotFoundError:
        pass

DEFAULT_WARNING_LIMIT = 3
DEFAULT_PUNISHMENT = "mute"  # Options: "mute", "ban"
DEFAULT_CONFIG = ("warn", DEFAULT_WARNING_LIMIT, DEFAULT_PUNISHMENT)

# Regex pattern to detect URLs in user bios
URL_PATTERN = re.compile(
    r'(https?://|www\.)[a-zA-Z0-9.\-]+(\.[a-zA-Z]{2,})+(/[a-zA-Z0-9._%+-]*)*'
)
