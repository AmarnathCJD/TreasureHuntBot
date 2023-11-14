from telethon import TelegramClient, events
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = os.getenv("API_KEY")
API_HASH = os.getenv("API_HASH")

if not all([BOT_TOKEN, API_ID, API_HASH]):
    raise Exception("Please set BOT_TOKEN, API_ID and API_HASH in .env file")

bot = TelegramClient('botv', API_ID, API_HASH)


import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')