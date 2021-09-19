# Leo Projects <https://t.me/leosupportx>
# @Naviya2 🇱🇰

import os
import time
import psutil
import shutil
import string
import asyncio
import config
from pyromod import listen
from asyncio import TimeoutError
from LeoSongDownloaderBot.translation import Translation
from helper.database.access_db import db
from helper.broadcast import broadcast_handler
from helper.database.add_user import AddUserToDatabase
from helper.display_progress import humanbytes, progress_for_pyrogram
from pyrogram import Client
from helper.forcesub import ForceSub
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types.bots_and_keyboards import reply_keyboard_markup
from LeoSongDownloaderBot.plugins import *
from LeoSongDownloaderBot.plugins import heroku_updater
from pyrogram import idle, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from LeoSongDownloaderBot import LeoSongDownloaderBot as app
from LeoSongDownloaderBot import LOGGER

STARTIMG = "https://telegra.ph/file/1af5a6a6d1cd420c75261.jpg"
HELP_IMG = "https://telegra.ph/file/7af5e5f9537e4bbe3461a.jpg"
ABOUTIMG= "https://telegra.ph/file/3a3d6c2bc0262d656fbf2.jpg"

@app.on_message(filters.private & filters.command("start"))
async def start(client, message):
    await AddUserToDatabase(client, message)
    FSub = await ForceSub(client, message)
    if FSub == 400:
        return
    await message.reply_photo(
        STARTIMG,
        caption=Translation.START_TEXT.format(message.from_user.mention),
        reply_markup=Translation.START_BUTTONS
    )
    
@app.on_message(filters.command(["help", f"help@leosongdownloaderbot"]))
async def help(client, message):
    await AddUserToDatabase(client, message)
    FSub = await ForceSub(client, message)
    if FSub == 400:
        return
    await message.reply_photo(
        HELP_IMG,
        caption="",
        reply_markup=Translation.HELP_BUTTONS
    )
 
@app.on_message(filters.command(["about", f"about@leosongdownloaderbot"]))
async def help(client, message):
    await AddUserToDatabase(client, message)
    FSub = await ForceSub(client, message)
    if FSub == 400:
        return
    await message.reply_photo(
        ABOUTIMG,
        caption="",
        reply_markup=Translation.ABOUT_BUTTONS
    )
    

    
@app.on_message(filters.private & filters.command("broadcast") & filters.user(config.BOT_OWNER) & filters.reply)
async def _broadcast(_, client: Message):
    await broadcast_handler(client)


@app.on_message(filters.private & filters.command("status") & filters.user(config.BOT_OWNER))
async def show_status_count(_, client: Message):
    total, used, free = shutil.disk_usage(".")
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    total_users = await db.total_users_count()
    await client.reply_text(
        text=f"**Total Disk Space:** {total} \n**Used Space:** {used}({disk_usage}%) \n**Free Space:** {free} \n**CPU Usage:** {cpu_usage}% \n**RAM Usage:** {ram_usage}%\n\n**Total Users in DB:** `{total_users}`\n\n@leosongdownloaderbot 🇱🇰",
        parse_mode="Markdown",
        quote=True
    )
@app.on_message()
async def welcome(client:Client, message:Message):
    if message.text in ["Hi", "Hello", "Hey", "hi", "hello", "hey", "HI", "HELLO", "HEY"]:
        await message.reply_text(
            text= f"**Hi** {message.from_user.first_name} 👋\n\n**How Are You ?? 😊**",
            parse_mode="md"
        )
    if message.text in ["Songs Download", "songs download", "songs down", "songs dwn", "Songs Dwn", "SONGS DOWNLOAD", "Songs download"]:
        await message.reply_text(
            text = f"**Hey** {message.from_user.mention}, **Do You Want To Download Songs ?**",
            reply_markup = InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("Yes 😊", callback_data="yes")
                ],[
                    InlineKeyboardButton("No ☹️", callback_data="no")
                ]]
            )
        )
app.start()
LOGGER.info("LeoSongDownloaderBot is online.")
idle()
