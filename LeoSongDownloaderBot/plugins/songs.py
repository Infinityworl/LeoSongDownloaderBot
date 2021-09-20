# Plugin by @Naviya2
# Leo Projects <https://t.me/new_ehi>


from __future__ import unicode_literals
import asyncio
import html
import os
import time
from random import randint
from urllib.parse import urlparse
from Python_ARQ import ARQ
from config import ARQ_API_KEY, UPDATES_CHANNEL, BOT_USERNAME
from LeoSongDownloaderBot import LeoSongDownloaderBot as app
import aiofiles
import aiohttp
import requests
import youtube_dl
from pyrogram import Client, filters
from LeoSongDownloaderBot.plugins.cb_buttons import cb_data
from helper.display_progress import progress_for_pyrogram, humanbytes, TimeFormatter
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from youtube_search import YoutubeSearch

is_downloading = False

aiohttpsession = aiohttp.ClientSession()

arq = ARQ("https://thearq.tech", ARQ_API_KEY, aiohttpsession)

@app.on_message(filters.command(['song', f'song@{BOT_USERNAME}']))
async def song(client, message):
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    await client.send_chat_action(chat_id=message.chat.id, action="typing")
    m = await message.reply_text('**Now I am Searching Your Song 🔎\n\nPlease Wait 😊**')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        #print(results)
        title = results[0]["title"][:40]       
        thumbnail = results[0]["thumbnails"][0]
        channel = results[0]["channel"][:50]
        thumb_name = f'thumb{title}.jpg'
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, 'wb').write(thumb.content)


        duration = results[0]["duration"]
        url_suffix = results[0]["url_suffix"]
        views = results[0]["views"]

    except Exception as err:
        await m.edit(
            "Nothing Found {} ☹️\n\nPlease check, you using correct format or your spellings are correct and try again 😊\n\nFormat : /song song_name 💫".format(message.from_user.mention)
        )
        print(str(err))
        return
    await m.edit("**Now I am Downloading Your Song ⏳\n\nPlease Wait 😊**")
    await client.send_chat_action(chat_id=message.chat.id, action="upload_audio")
    await asyncio.sleep(3)
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f'🎙**Title**: `{title[:35]}`\n🎵 **Source** : `Youtube`\n⏱️ **Song Duration**: `{duration}`\n👁‍🗨 **Song Views**: `{views}`\n🗣 **Released By** :` {channel}`\n\n**Downloaded By** : @leosongdownloaderbot 🇱🇰'
        start_time = time.time()
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
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
    except Exception as e:
        await asyncio.sleep(2)
        await m.edit_text(text=f"{e}\n\nChat ID : [{message.chat.id}](tg://chat?id={message.chat.id}) 🎗", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Report To Owner 🧑‍💻", callback_data="report_to_owner")]]))
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

# Jiosaavn Music Downloader
@app.on_message(filters.command(['saavn', f'saavn@{BOT_USERNAME}']) & ~filters.edited)
async def jssong(_, message):
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
        await asyncio.sleep(3)
        await m.edit("**Now I am Uploading Your Song ⏳\n\nPlease Wait 😊**")
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
        await m.edit_text(text=f"{e}\n\nChat ID : [{message.chat.id}](tg://chat?id={message.chat.id}) 🎗", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Report To Owner 🧑‍💻", callback_data="report_to_owner")]]))
        return
    is_downloading = False

# currently not working  !!
@app.on_message(filters.command('deezer') & ~filters.edited)
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
@app.on_message(filters.command(['lyrics', f'lyrics@{BOT_USERNAME}']))
async def lyrics_func(_, message):
    if len(message.command) < 2:
        await message.reply_text("{},\n\nUse this format to get lyrics 👇\n\n<code>/lyrics song_name</code>".format(message.from_user.mention))
        return
    m = await message.reply_text("**Now I am Searching Lyrics Related to Your Song Name🔎\n\nPlease Wait 😊**")
    query = message.text.strip().split(None, 1)[1]
    song = await arq.lyrics(query)
    lyrics = song.result
    if len(lyrics) < 4095:
        await m.edit(f"__{lyrics}__")
        return
    lyrics = await paste(lyrics)
    await m.edit(f"**Sorry {message.from_user.mention},\n\nI cannot upload lyrics to telegram becz You requested song's lyrics are too long !!\n\nBut you can get your lyrics from the below link😊\n**Your Song Lyrics: [Click Here]({lyrics})**")
