import logging

from pyrogram import (
    Client,
    enums,
    __version__
)

from config import (
    API_HASH,
    API_ID,
    TG_USER_SESSION,
)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

LOGGER = logging.getLogger(__name__)


class User(Client):
    def __init__(self):
        super().__init__(
            name="LeoSongDLUserBot",
            session_string=TG_USER_SESSION,
            api_hash=API_HASH,
            api_id=API_ID,
            workers=4
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        return (self, usr_bot_me.id)
    
    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Leo Song Downloader Bot's Assistent stopped. Bye.")
