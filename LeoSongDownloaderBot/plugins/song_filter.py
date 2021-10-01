import re
import asyncio
import pyrogram
from config import MAINCHANNEL_ID
from LeoSongDownloaderBot import Bot
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

async def SongsFilter(client: Bot, message: Message): 
    try:
        async for msg in client.USER.search_messages(MAINCHANNEL_ID,query=message.text[5:], filter="audio", limit=1):
            message_id = msg.message_id   
            await message.reply_chat_action("upload_audio")                  
            x=await message.reply_text("**Now I'm Downloading ⏳**")
            await x.edit("Now I'm Uploading 💫")

            if message.chat.id == message.from_user.id:
                await client.copy_message(
                    chat_id=message.chat.id,
                    from_chat_id=MAINCHANNEL_ID,
                    message_id=message_id,
                    reply_markup=InlineKeyboardMarkup(
                        [[
                            InlineKeyboardButton("Requested By ❓",url=f"https://t.me/{message.from_user.username}")
                        ],[
                            InlineKeyboardButton("Send To Channel / Group 🧑‍💻", callback_data="sendtochannel")
                        ]]
                    )
                )
            else:
                await client.copy_message(
                    chat_id=message.chat.id,
                    from_chat_id=MAINCHANNEL_ID,
                    message_id=message_id,
                    reply_markup=InlineKeyboardMarkup(
                        [[
                            InlineKeyboardButton("Send To Bot's PM 💫", callback_data="sendtoib")
                        ],[
                            InlineKeyboardButton("Requested By ❓", url="https://t.me/{message.from_user.username}")
                        ]]
                    )
                )
            await x.delete()
            return 200
    except:
        return 400