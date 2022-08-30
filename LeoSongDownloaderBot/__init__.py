# Leo Projects <https://t.me/leosupportx>

import logging

from pyrogram import Client
from pyromod import listen
from LeoSongDownloaderBot.userbot import User
from config import API_HASH, API_ID, BOT_TOKEN

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

LOGGER = logging.getLogger(__name__)

class Bot(Client):
    USER: User = None
    USER_ID: int = None

    def __init__(self):
        super().__init__(
            name="LeoSongDownloaderBotX",
            api_hash=API_HASH,
            api_id=API_ID,
            plugins={
                "root": "LeoSongDownloaderBot/plugins"
            },
            bot_token=BOT_TOKEN,
            sleep_threshold=300
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.USER, self.USER_ID = await User().start()
        await self.USER.send_message(
            chat_id=usr_bot_me.username,
            text="😬🤒🤒"
        )
        self.LOGGER.info("Assitant Started !!")

    async def stop(self, *args):
        await super().stop()
        self.LOGGER.info("Bot stopped. Bye.")
