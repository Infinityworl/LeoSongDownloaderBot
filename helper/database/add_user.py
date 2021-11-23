import config
from helper.database.access_db import db
from pyrogram import Client
from pyrogram.types import Message


async def AddUserToDatabase(bot: Client, cmd: Message):
    if not await db.is_user_exist(cmd.chat.id):
        await db.add_user(cmd.chat.id)
        if config.LOG_CHANNEL is not None:
            await bot.send_message(
                int(config.LOG_CHANNEL),
                f"#NEW_USER: \n\nNew User [{cmd.chat.title}](tg://user?id={cmd.chat.id}) started @{(await bot.get_me()).username} !!"
            )
