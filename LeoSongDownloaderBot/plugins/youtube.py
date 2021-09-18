import os
import time
import asyncio
from urllib.parse import urlparse
from pyrogram import Client, client, filters
from helper.display_progress import humanbytes, progress_for_pyrogram
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from youtube_dl import YoutubeDL
from opencc import OpenCC
from LeoSongDownloaderBot import LeoSongDownloaderBot

YTDL_REGEX = (r"^((?:https?:)?\/\/)"
              r"?((?:www|m)\.)"
              r"?((?:youtube\.com|youtu\.be))"
              r"(\/)([-a-zA-Z0-9()@:%_\+.~#?&//=]*)([\w\-]+)(\S+)?$")
s2tw = OpenCC('s2tw.json').convert

@LeoSongDownloaderBot.on_message(filters.text
                   & ~filters.edited
                   & filters.regex(YTDL_REGEX))
async def ytdl_with_button(client: Client, message: Message):
    await client.send_chat_action(chat_id=message.chat.id, action="typing")
    await message.reply_text(
        "**Please click the below button to download your song 😊**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Download 🎵",
                        callback_data="ytdl_audio"
                    )
                ]
            ]
        ),
        quote=True
    )

@LeoSongDownloaderBot.on_callback_query(filters.regex("^ytdl_audio$"))
async def callback_query_ytdl_audio(_, callback_query):
    try:
        url = callback_query.message.reply_to_message.text
        ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': '%(title)s - %(extractor)s-%(id)s.%(ext)s',
            'writethumbnail': True
        }
        with YoutubeDL(ydl_opts) as ydl:
            message = callback_query.message
            info_dict = ydl.extract_info(url, download=False)
            # download
            await message.reply_chat_action(action="upload_audio")
            await callback_query.edit_message_text("**Now I am Downloading Your Song ⏳\n\nPlease Wait 😊**")
            ydl.process_info(info_dict)
            # upload
            audio_file = ydl.prepare_filename(info_dict)
            basename = audio_file.rsplit(".", 1)[-2]
             # .webm -> .weba
            if info_dict['ext'] == 'webm':
                audio_file_weba = basename + ".weba"
                os.rename(audio_file, audio_file_weba)
                audio_file = audio_file_weba
            # thumbnail
                thumbnail_url = info_dict['thumbnail']
                thumbnail_file = basename + "." + \
                get_file_extension_from_url(thumbnail_url)
            # info (s2tw)
            webpage_url = info_dict['webpage_url']
            title = s2tw(info_dict['title'])
            duration = int(float(info_dict['duration']))
            performer = s2tw(info_dict['uploader'])
            caption = f"🎙**Title**: `{title[:35]}`\n🎵 **Source** : `Youtube`\n⏱️ **Song Duration**: `{duration}`\n\n**Downloaded By** : **@leosongdownloaderbot 🇱🇰**"
            start_time = time.time()
    
            if callback_query.message.chat.id == callback_query.from_user.id:
                await message.reply_audio(
                    audio=audio_file,
                    caption=caption,
                    duration=duration,
                    performer=performer,
                    title=title,
                    progress=progress_for_pyrogram,
                    progress_args=(
                    "Downloading Song 🎵",
                    message,
                    start_time
                    ),  
                    parse_mode='md',
                    thumb=thumbnail_file,
                    reply_markup=InlineKeyboardMarkup(
                        [[
                            InlineKeyboardButton("Requested By ❓", url=f"https://t.me/{message.from_user.username}")
                        ],[
                            InlineKeyboardButton("Send To Channel / Group 🧑‍💻", callback_data="sendtochannel")
                        ],[
                            InlineKeyboardButton("Open In Youtube 💫", url=webpage_url)
                        ]]
                    )
                )
            else:
                await message.reply_audio(
                    audio=audio_file,
                    caption=caption,
                    duration=duration,
                    performer=performer,
                    title=title,
                    progress=progress_for_pyrogram,
                    progress_args=(
                    "Downloading Song 🎵",
                    message,
                    start_time
                    ),  
                    parse_mode='HTML',
                    thumb=thumbnail_file,
                    reply_markup=InlineKeyboardMarkup(
                        [[
                            InlineKeyboardButton("Send To Bot's PM 💫", callback_data="sendtoib")
                        ],[
                            InlineKeyboardButton("Requested By ❓", url="https://t.me/{message.from_user.username}")
                        ],[
                            InlineKeyboardButton("Open In Youtube 💫", url=webpage_url)
                        ]]
                    )
                )
            await callback_query.message.delete()
    except Exception as e:
        await message.reply_text(text=e, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Report To Owner 🧑‍💻", callback_data="report_to_owner")]]))
        print (e)
    os.remove(audio_file)
    os.remove(thumbnail_file)

def get_file_extension_from_url(url):
    url_path = urlparse(url).path
    basename = os.path.basename(url_path)
    return basename.split(".")[-1]
