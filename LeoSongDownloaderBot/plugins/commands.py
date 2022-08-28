# Plugin by @Naviya2
# Leo Projects <https://t.me/new_ehi>


from __future__ import unicode_literals
import asyncio
import shutil
import psutil
import config
import html
import os
import time
from random import randint
from urllib.parse import urlparse
from Python_ARQ import ARQ
from config import ARQ_API_KEY, UPDATES_CHANNEL, BOT_USERNAME
import aiofiles
import aiohttp
import requests
import yt_dlp
from pyrogram import Client, filters
from LeoSongDownloaderBot.plugins.cb_buttons import cb_data
from helper.display_progress import progress_for_pyrogram, humanbytes, TimeFormatter
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from youtube_search import YoutubeSearch
from LeoSongDownloaderBot.plugins.song_filter import SongsFilterForCommandDL, SongsFilterForPMDL
from LeoSongDownloaderBot import Bot
from LeoSongDownloaderBot.translation import Translation
from helper.forcesub import ForceSub
from helper.database.access_db import db
from helper.broadcast import broadcast_handler
from helper.database.add_user import AddUserToDatabase


is_downloading = False

aiohttpsession = aiohttp.ClientSession()

arq = ARQ("http://arq.hamker.dev", ARQ_API_KEY, aiohttpsession)

@Client.on_message(filters.command(['song', f'song@{BOT_USERNAME}']))
async def song(client: Client, message: Message):
    await AddUserToDatabase(client, message)
    FSub = await ForceSub(client, message)
    if FSub == 400:
        return
    FilterSongs = await SongsFilterForCommandDL(client, message)
    if FilterSongs == 200:
        return  
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        #print(results)
        title = results[0]["title"]       
        thumbnail = results[0]["thumbnails"][0]
        channel = results[0]["channel"][:50]
        thumb_name = f'thumb{title}.jpg'
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, 'wb').write(thumb.content)


        duration = results[0]["duration"]
        url_suffix = results[0]["url_suffix"]
        views = results[0]["views"]
    
        m = await message.reply_text("**Now I am Searching Your Song ⏳\n\nPlease Wait 😊**")

    except Exception as err:
        await message.reply_text(
            "Nothing Found {} ☹️\n\nPlease check, you using correct format or your spellings are correct and try again 😊\n\nFormat : /song song_name 💫".format(message.from_user.mention)
        )
        print(str(err))
        return
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(link, download=False)
                size = int(info_dict["filesize"])

                if size/1024/1024 > 50:
                    await message.reply_text(
                        text=f"**Hey** {message.from_user.mention},\n\n**I Can't Download Song That You Requested 😒**\n**Reason Is I can't Upload Songs Than 50MB To Telegram Because OF Telegram API Limit**\n\n **You Requested Song's Size :** **{size/1024//1024}** **MB** 😑",
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close ❌", callback_data="close")]])
                    )
                
                else:
                    await m.edit("**Now I am Downloading Your Song ⏳\n\nPlease Wait 😊**")
                    ydl.process_info(info_dict)
                    audio_file = ydl.prepare_filename(info_dict)
                    await client.send_chat_action(chat_id=message.chat.id, action="upload_audio") 
                    rep = f'🎙**Title**: `{title}`\n🎵 **Source** : `Youtube`\n⏱️ **Song Duration**: `{duration}`\n👁‍🗨 **Song Views**: `{views}`\n🗣 **Released By** :` {channel}`\n\n**Downloaded By** : @leosongdownloaderbot 🇱🇰'
                    start_time = time.time()
                    secmul, dur, dur_arr = 1, 0, duration.split(':')
                    for i in range(len(dur_arr)-1, -1, -1):
                        dur += (int(dur_arr[i]) * secmul)
                        secmul *= 60
                    await client.send_audio(
                        chat_id=-1001571768793,
                        audio=audio_file,
                        caption=rep,
                        thumb=thumb_name,
                        title=title,
                        duration=dur
                    )
                    if message.chat.id == message.from_user.id:
                            await message.reply_audio(
                            audio=audio_file, 
                            caption=rep,
                            progress=progress_for_pyrogram,
                            progress_args=(
                                "Downloading Song 🎵",
                                m,
                                start_time
                            ),  
                            thumb=thumb_name, 
                            parse_mode="md", 
                            title=title,
                            duration=dur,
                            reply_markup=InlineKeyboardMarkup(
                                [[
                                    InlineKeyboardButton("Requested By ❓",url=f"https://t.me/{message.from_user.username}")
                                ],[
                                    InlineKeyboardButton("Send To Channel / Group 🧑‍💻", callback_data="sendtochannel")
                                ],[
                                    InlineKeyboardButton("Open In Youtube 💫", url=link)
                                ]]
                            )
                        )
                    else:
                        await message.reply_audio(
                        audio=audio_file, 
                        caption=rep,
                        progress=progress_for_pyrogram,
                        progress_args=(
                            "Downloading Song 🎵",
                            m,
                            start_time),  
                        thumb=thumb_name, 
                        parse_mode="md", 
                        title=title,
                        duration=dur,
                        reply_markup=InlineKeyboardMarkup(
                            [[
                                InlineKeyboardButton("Send To Bot's PM 💫", callback_data="sendtoib")
                            ],[
                                InlineKeyboardButton("Requested By ❓", url="https://t.me/{message.from_user.username}")
                            ],[
                                InlineKeyboardButton("Open In Youtube 💫", url=link)
                            ]]
                        )
                    )
                    await m.delete()
                    try:
                        os.remove(audio_file)
                        os.remove(thumb_name)
                    except Exception as e:
                        print(e)
    except Exception as e:
        await m.edit_text(text=f"{e}\n\nChat ID : <code>{message.chat.id}</code> 🎗\n\nChat Mention : [{message.chat.title}](https://t.me/{message.chat.username}) ", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Report To Owner 🧑‍💻", callback_data="report_to_owner")]]))
        print(e)

#Download In Pm Without Any Command 


#This is for jiosaavn downloader
async def download_song(url):
    song_name = f"{randint(6969, 6999)}.mp3"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(song_name, mode="wb")
                await f.write(await resp.read())
                await f.close()
    return song_name

# Jiosaavn Music Downloader
@Client.on_message(filters.command(['saavn', f'saavn@{BOT_USERNAME}']))
async def jssong(client, message):
    FSub = await ForceSub(client, message)
    if FSub == 400:
        return
    global is_downloading
    if len(message.command) < 2:
        await message.reply_text("{},\n\nUse this format to download songs from saavn 👇\n\n<code>/saavn song_name</code>".format(message.from_user.mention))
        return
    if is_downloading:
        await message.reply_text(
            "{},\n\nAnother download is in progress now ⏳\n\nPlease try again after 1 or 2 minutes 😊".format(message.from_user.mention)
        )
        return
    is_downloading = True
    text = message.text.split(None, 1)[1]
    query = text.replace(" ", "%20")
    m = await message.reply_text("**Now I am Searching Your Song 🔎\n\nPlease Wait 😊**")
    try:
        songs = await arq.saavn(query)
        if not songs.ok:
            await message.reply_text(songs.result)
            return
        sname = songs.result[0].song
        slink = songs.result[0].media_url
        ssingers = songs.result[0].singers
        start_time = time.time()
        cap = "🎵 <b>Source</b> : <code>Saavn</code>\n\n<b>Downloaded By</b> : @leosongdownloaderbot 🇱🇰"
        await m.edit("**Now I am Downloading Your Song ⏳\n\nPlease Wait 😊**")
        song = await download_song(slink)
        await m.edit("**Now I am Uploading Your Song ⏳\n\nPlease Wait 😊**")
        await client.send_audio(
                chat_id=-1001571768793,
                audio=song,
                caption=cap,
                title=sname,
                performer=ssingers
        )
        if message.chat.id == message.from_user.id:
            await message.reply_audio(
                audio=song,
                title=sname,
                caption=cap,
                progress=progress_for_pyrogram,
                progress_args=(
                    "Downloading Song 🎵 ",
                    m,
                    start_time),
                performer=ssingers,
                reply_markup=InlineKeyboardMarkup(
                    [[
                        InlineKeyboardButton("Requested By ❓",url=f"https://t.me/{message.from_user.username}")
                    ],[
                        InlineKeyboardButton("Send To Channel / Group 🧑‍💻", callback_data="sendtochannel")
                    ]]
                )
            )
        else:
            await message.reply_audio(
                audio=song,
                title=sname,
                caption=cap,
                progress=progress_for_pyrogram,
                progress_args=(
                    "Downloading Song 🎵 ",
                    m,
                    start_time),
                performer=ssingers,
                reply_markup=InlineKeyboardMarkup(
                    [[
                        InlineKeyboardButton("Send To Bot's PM 💫", callback_data="sendtoib")
                    ],[
                        InlineKeyboardButton("Requested By ❓", url="https://t.me/{message.from_user.username}")
                    ]]
                )
            )

        os.remove(song)
        await m.delete()
    except Exception as e:
        is_downloading = False
        await m.edit_text(text=f"{e}\n\nChat ID : <code>{message.chat.id}</code> 🎗", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Report To Owner 🧑‍💻", callback_data="report_to_owner")]]))
        return
    is_downloading = False

# currently not working  !!
@Client.on_message(filters.command('deezer'))
async def deezsong(client, message):
    global is_downloading
    if len(message.command) < 2:
        await message.reply_text("{},\n\nUse this format to download songs from deezer 👇\n\n<code>/deezer song_name</code>".format(message.from_user.mention))
        return
    if is_downloading:
        await message.reply_text(
            "{},\n\nAnother download is in progress now ⏳\n\nPlease try again after 1 or 2 minutes 😊".format(message.from_user.mention)
        )
        return
    is_downloading = True
    text = message.text.split(None, 1)[1]
    query = text.replace(" ", "%20")
    m = await message.reply_text("**Now I am Searching Your Song 🔎\n\nPlease Wait 😊**")
    try:
        songs = await arq.deezer(query, 1)
        if not songs.ok:
            await message.reply_text(songs.result)
            return
        title = songs.result[0].title
        url = songs.result[0].url
        artist = songs.result[0].artist
        start_time = time.time()
        cap = "🎵 <b>Source</b> : <code>Deezer</code>\n\n<b>Downloaded By</b> : @leosongdownloaderbot 🇱🇰"
        await m.edit("Now I am Downloading Your Song ⏳\n\nPlease Wait 😊")
        song = await download_song(url)
        await client.send_chat_action(chat_id=message.chat.id, action="upload_audio")
        await m.edit("Now I am Uploading Your Song ⏳\n\nPlease Wait 😊")
        await message.reply_audio(audio=song, caption=cap, title=title, performer=artist)
        os.remove(song)
        await m.delete()
    except Exception as e:
        is_downloading = False
        await m.edit(str(e))
        return
    is_downloading = False

# Song Lyrics Downloader
@Client.on_message(filters.command(['lyrics', f'lyrics@{BOT_USERNAME}']))
async def lyrics_func(client, message):
    FSub = await ForceSub(client, message)
    if FSub == 400:
        return
    if len(message.command) < 2:
        await message.reply_text("{},\n\nUse this format to get lyrics 👇\n\n<code>/lyrics song_name</code>".format(message.from_user.mention))
        return
    m = await message.reply_text("**Now I am Searching Lyrics Related to Your Song Name🔎\n\nPlease Wait 😊**")
    query = message.text.strip().split(None, 1)[1]
    song = await arq.lyrics(query)
    lyrics = song.result
    if len(lyrics) < 4095:
        await m.edit(f"__{lyrics}__")
    else:
        await m.edit(f"**Sorry {message.from_user.mention},\n\nI cannot upload lyrics to telegram becz You requested song's lyrics are too long !!\n\nBut you can get your lyrics from the below link😊\n**Your Song Lyrics: [Click Here]({lyrics})**")

STARTIMG = "https://telegra.ph/file/1af5a6a6d1cd420c75261.jpg"
HELP_IMG = "https://telegra.ph/file/7af5e5f9537e4bbe3461a.jpg"
ABOUTIMG= "https://telegra.ph/file/3a3d6c2bc0262d656fbf2.jpg"

@Client.on_message(filters.private & filters.command("start"))
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
    
@Client.on_message(filters.command(["help", f"help@leosongdownloaderbot"]))
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
 
@Client.on_message(filters.command(["about", f"about@leosongdownloaderbot"]))
async def about(client, message):
    await AddUserToDatabase(client, message)
    FSub = await ForceSub(client, message)
    if FSub == 400:
        return
    await message.reply_photo(
        ABOUTIMG,
        caption="",
        reply_markup=Translation.ABOUT_BUTTONS
    )
    

    
@Client.on_message(filters.private & filters.command("broadcast") & filters.user(config.BOT_OWNER) & filters.reply)
async def _broadcast(_, client: Message):
    await broadcast_handler(client)


@Client.on_message(filters.private & filters.command("status") & filters.user(config.BOT_OWNER))
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

@Client.on_message()
async def welcome(client: Client, message: Message):
    if message.text in ["Hi", "Hello", "Hey", "hi", "hello", "hey", "HI", "HELLO", "HEY"]:
        await message.reply_text(f"**Hi** {message.from_user.mention} 👋\n\n**How Are You ??**")
    if message.text in ["Songs Download", "songs download", "songs down", "songs dwn", "Songs Dwn", "SONGS DOWNLOAD", "Songs download", "song download"]:
        await message.reply_text(
            text = f"**Hey** {message.from_user.mention}, **Do You Want To Download Songs ?**",
            reply_markup = InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("Yes 😊", callback_data="help")
                ],[
                    InlineKeyboardButton("No ☹️", callback_data="no")
                ]]
            )
        )
