import os
import time
import asyncio
import datetime
import pytz
import requests
from urllib.parse import urlparse
from pyromod import listen
from LeoSongDownloaderBot.translation import Translation
import config
from helper.database.access_db import db
from pyrogram import Client, filters
from asyncio import TimeoutError
from pyrogram.errors import UserNotParticipant
import yt_dlp
from opencc import OpenCC
from pyrogram import enums
from helper.forcesub import ForceSub
from helper.display_progress import humanbytes, progress_for_pyrogram
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, Message, ForceReply
from LeoSongDownloaderBot import Client as app

#for yt dl cb
YTDL_REGEX = (r"^((?:https?:)?\/\/)"
              r"?((?:www|m)\.)"
              r"?((?:youtube\.com|youtu\.be))"
              r"(\/)([-a-zA-Z0-9()@:%_\+.~#?&//=]*)([\w\-]+)(\S+)?$")
s2tw = OpenCC('s2tw.json').convert

@app.on_message(filters.text
                   & filters.regex(YTDL_REGEX))
async def ytdl_with_button(client: Client, message: Message):
    await client.send_chat_action(chat_id=message.chat.id, action=enums.ChatAction.UPLOAD_AUDIO)
    FSub = await ForceSub(client, message)
    if FSub == 400:
        return
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

def get_file_extension_from_url(url):
    url_path = urlparse(url).path
    basename = os.path.basename(url_path)
    return basename.split(".")[-1]

@app.on_callback_query(filters.regex("^ytdl_audio$"))
async def callback_query_ytdl_audio(client, callback_query):
    try:
        url = callback_query.message.reply_to_message.text
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]',
            'outtmpl': '%(title)s - %(extractor)s-%(id)s.%(ext)s',
            'writethumbnail': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            message = callback_query.message
            info_dict = ydl.extract_info(url, download=False)
            size = int(info_dict["filesize"])
        
            if size/1024/1024 > 50:
                await message.reply_text(
                        text=f"**Hey** {callback_query.from_user.mention},\n\n**I Can't Download Song That You Requested 😒**\n**Reason Is I can't Upload Songs Than 50MB To Telegram Because OF Telegram API Limit**\n\n **You Requested Song's Size :** **{size/1024/1024}** **MB** 😑",
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close ❌", callback_data="close")]])
                )                 
            else:
            # download
                await callback_query.message.reply_chat_action(action=enums.ChatAction.UPLOAD_AUDIO)
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
                  
            # info (s2tw)
                webpage_url = info_dict['webpage_url']
                title = s2tw(info_dict['title'])
                thumbnail_url = info_dict[0]["thumbnails"]
                thumbnail_file = basename + "." + \
                get_file_extension_from_url(thumbnail_url)
                duration = str(info_dict['duration'])
                performer = s2tw(info_dict['uploader'])
                caption = f"🎙**Title**: `{title}`\n🎵 **Source** : `Youtube`\n\n**Downloaded By** : **@leosongdownloaderbot 🇱🇰**"
                start_time = time.time()
                secmul, dur, dur_arr = 1, 0, duration.split(':')
                for i in range(len(dur_arr)-1, -1, -1):
                    dur += (int(dur_arr[i]) * secmul)
                    secmul *= 60
                await client.send_audio(
                        chat_id=-1001571768793,
                        audio=audio_file,
                        caption=caption,
                        thumb=thumbnail_file,
                        title=title,
                        duration=dur
                    )
                if callback_query.message.chat.id == callback_query.from_user.id:
                    await message.reply_audio(
                        audio=audio_file,
                        caption=caption,
                        duration=dur,
                        performer=performer,
                        title=title,
                        progress=progress_for_pyrogram,
                        progress_args=(
                            "Downloading Song 🎵",
                            message,
                            start_time
                        ),  
                        parse_mode=enums.ParseMode.MARKDOWN,
                        thumb=thumbnail_file,
                        reply_markup=InlineKeyboardMarkup(
                            [[
                                InlineKeyboardButton("Requested By ❓", url=f"https://t.me/{callback_query.from_user.username}")
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
                        performer=performer,
                        duration=dur,
                        title=title,
                        progress=progress_for_pyrogram,
                        progress_args=(
                            "Downloading Song 🎵",
                            message,
                            start_time
                        ),  
                        parse_mode=enums.ParseMode.HTML,
                        thumb=thumbnail_file,
                        reply_markup=InlineKeyboardMarkup(
                            [[
                                InlineKeyboardButton("Send To Bot's PM 💫", callback_data="sendtoib")
                            ],[
                                InlineKeyboardButton("Requested By ❓", url="https://t.me/{callback_query.from_user.username}")
                            ],[
                                InlineKeyboardButton("Open In Youtube 💫", url=webpage_url)
                            ]]
                        )
                    )
                await callback_query.message.delete()
                try:
                    os.remove(audio_file)
                    os.remove(thumbnail_file)
                except Exception as e:
                    print(e)
    except Exception as e:
        await callback_query.message.reply_text(text=e, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Report To Owner 🧑‍💻", callback_data="report_to_owner")]]))
        print (e)

@app.on_callback_query()
async def cb_data(Client, msg:CallbackQuery):
    if msg.data == "home":
        await msg.message.edit_text(
            text=Translation.START_TEXT.format(msg.from_user.mention),
            reply_markup=Translation.START_BUTTONS,
            disable_web_page_preview=True
        )
    elif msg.data == "sendtoib":
        await Client.forward_messages(
            from_chat_id=msg.message.chat.id,
            chat_id=msg.from_user.id, 
            message_ids=msg.message.id
        )
        await msg.answer(f"{msg.from_user.first_name} ,Successfully Sent To Your PM 💫", show_alert=False)
    
    elif msg.data == "report_to_owner":
        await Client.forward_messages(
            from_chat_id=msg.message.chat.id,
            chat_id=-1001523985078, 
            message_ids=msg.message.id
        )
        await msg.answer(f"{msg.from_user.first_name}, Successfully Reported To Owner 💫", show_alert=False)
        await asyncio.sleep(3)
        await msg.message.delete()
    
    elif msg.data == "sendtochannel":
        await msg.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("Note ❗️ ", callback_data="ingrpchnl")
                ],[
                    InlineKeyboardButton("Group 💬", callback_data="group")
                ],[
                    InlineKeyboardButton("Channel 💫", callback_data="channel")
                ]]
            )
        )

    elif msg.data == "group":
        await msg.answer(f"Hey {msg.from_user.first_name},\n\nPlease Make Sure Leo Song Downloader Bot Is Promoted As Admin In Your Group 😊", show_alert=True)
        await Client.send_message(
            text="Please Enter Your Group ID : ",
            chat_id=msg.message.chat.id,
            reply_to_message_id=msg.message.id,
            reply_markup=ForceReply()
        )
        try:
            ask_ : Message = await Client.listen(msg.message.chat.id, timeout=300)
            if ask_.text.startswith("-100"):
                pass
            else:
                await msg.message.reply_text(
                    text=f"<b>Sorry</b> {msg.from_user.mention} !\n\n <b>You Entered</b> <code>{ask_.text}</code> <b>Is Not Correct Group Id 😐</b>\n\n<b>It is not Started With '-100 ' 😒</b>",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Retry 💫", callback_data="group")],[InlineKeyboardButton("Close ❌", callback_data="close")]]),
                    parse_mode=enums.ParseMode.HTML
                )
            if len(ask_.text) >= 13:
                pass
            else:
                missed_words = 14 - len(ask_.text)
                await msg.message.reply_text(
                    text=f"<b>Sorry</b> {msg.from_user.mention} !\n\n <b>You Entered</b> <code>{ask_.text}</code> <b>Is Not Correct Group Id 😐</b>\n\n<b>It Missed {missed_words} Words ❗</b>",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Retry 💫", callback_data="group")],[InlineKeyboardButton("Close ❌", callback_data="close")]]),
                    parse_mode=enums.ParseMode.HTML
                )
        except TimeoutError:
            await msg.answer(f"Sorry {msg.from_user.first_name}, Sorry Timed Out !!", show_alert=False)
        
        await Client.forward_messages(
            from_chat_id=msg.message.chat.id,
            chat_id=int(ask_.text), 
            message_ids=msg.message.id
        )
        await msg.message.reply_text(
            text=f"**Successfully Forwarded To** {ask_.text} 😊",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close ❌", callback_data="close")]])
        )
    elif msg.data == "ingrpchnl":
        await msg.answer(f"{msg.from_user.first_name},\nLeo Song Downloader Bot Should Be Promoted As ADMIN In The Group / Channel To Forward Messages 😊", show_alert=True)
    
    elif msg.data == "channel":
        await msg.answer(f"Hey {msg.from_user.first_name},\n\nPlease Make Sure Leo Song Downloader Bot Is Promoted As Admin In Your Channel 😊", show_alert=True)
        await Client.send_message(
            text="Please Enter Your Channel ID : ",
            chat_id=msg.message.chat.id,
            reply_to_message_id=msg.message.id,
            reply_markup=ForceReply()
        )
        try:
            ask_ : Message = await Client.listen(msg.message.chat.id, timeout=300)
            if ask_.text.startswith("-100"):
                pass
            else:
                await msg.message.reply_text(
                    text=f"<b>Sorry</b> {msg.from_user.mention} !\n\n <b>You Entered</b> <code>{ask_.text}</code> <b>Is Not Correct Channel Id 😐</b>\n\n<b>Because It is not Started With '-100 ' 😒</b>",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Retry 💫", callback_data="channel")],[InlineKeyboardButton("Close ❌", callback_data="close")]]),
                    parse_mode=enums.ParseMode.HTML
                )
            if len(ask_.text) >= 13:
                pass
            else:
                missed_words = 14 - len(ask_.text)
                await msg.message.reply_text(
                    text=f"<b>Sorry</b> {msg.from_user.mention} !\n\n <b>You Entered</b> <code>{ask_.text}</code> <b>Is Not Correct Channel Id 😐</b>\n\n<b>It Missed {missed_words} Words ❗</b>",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Retry 💫", callback_data="group")],[InlineKeyboardButton("Close ❌", callback_data="close")]]),
                    parse_mode="html"
                )
        except TimeoutError:
                await msg.answer(f"Sorry {msg.from_user.first_name}, Timed Out !!", show_alert=False)
        
        await Client.forward_messages(
            from_chat_id=msg.message.chat.id,
            chat_id=int(ask_.text), 
            message_ids=msg.message.id
        )
        await msg.message.reply_text(
            text=f"**Successfully Forwarded To** {ask_.text} 😊",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close ❌", callback_data="close")]])
        )
    elif msg.data == "help":
        await msg.message.edit_media(media=InputMediaPhoto("https://telegra.ph/file/7af5e5f9537e4bbe3461a.jpg", caption=""),
            reply_markup=Translation.HELP_BUTTONS
        )
    elif msg.data == "help_for_yt":
        await msg.answer(f"{msg.from_user.first_name},\n\nSend Your Song Name Directly To The Bot's PM To Download Songs(No Need Any Command For For Download Songs In Bot's PM)\n\nPlease Use The Below Format To Download Songs From YouTube In Groups😊\n\nFormat : /song song_name 💫", show_alert=True)
    
    elif msg.data == "help_for_saavn":
        await msg.answer(f"{msg.from_user.first_name},\n\nPlease Use The Below Format To Download Songs From Saavn 😊\n\nFormat : /saavn song_name 💫", show_alert=True)
    
    elif msg.data == "help_for_lyrics_down":
        await msg.answer(f"{msg.from_user.first_name},\n\nPlease Use The Below Format To Download Lyrics 😊\n\nFormat : /lyrics song_name 💫", show_alert=True)

    elif msg.data == "help_for_url_dl":
        await msg.answer(f"{msg.from_user.first_name},\n\nSimply Copy An Url From YT and Paste It On This Bot 😊" , show_alert=True)
    
    elif msg.data == "bot_users_count":
        user_count = await db.total_users_count()
        dt = datetime.datetime.now(pytz.timezone("UTC")).strftime("%I:%M %p %d/%m/%y") 
        dtsl = datetime.datetime.now(pytz.timezone("Asia/Colombo")).strftime("%I:%M %p %d/%m/%y")
        await msg.answer(f"Hi {msg.from_user.first_name} 👋\n\nTotal Users : {user_count} 💫\n\nLast Update :\n {dt} (UTC 🌎)\n {dtsl} (Sri Lanka 🇱🇰)\n\nShare And Support Us 😊", show_alert=True)
    
    elif msg.data == "no":
        await msg.message.edit_text(text = f"{msg.from_user.mention},\n\n<b>Sorry For Disturbing You ☹️</b>")
        await asyncio.sleep(2)
        await msg.message.delete()

    elif msg.data == "about":
        await msg.message.edit_media(media=InputMediaPhoto("https://telegra.ph/file/3a3d6c2bc0262d656fbf2.jpg", caption=""),
            reply_markup=Translation.ABOUT_BUTTONS 
        )
    elif msg.data == "about_bot":
        await msg.message.edit_media(media=InputMediaPhoto("https://telegra.ph/file/0a74f0d99895100076640.jpg", caption=Translation.ABOUT_TEXT),
            reply_markup=Translation.ABOUT_BOT_BUTTONS
        )
    elif msg.data == "aboutdev":
        await msg.message.edit_media(media=InputMediaPhoto("https://telegra.ph/file/bafeaf3fb8119b136b781.jpg", caption=""),
        reply_markup=Translation.ABOUT_DEV_BUTTONS
        )
    elif msg.data == "aboutdevtext":
        await msg.answer("Developer is a Super Noob 😅\n\nIf you find any bug on this bot, Please be kind to tell him 😊", show_alert=True)

    elif msg.data == "user_info":
        await msg.message.edit_media(media=InputMediaPhoto("https://telegra.ph/file/4a3960b085743a6f1bf32.jpg", caption=Translation.INFO_TEXT.format(username=msg.from_user.username, first_name=msg.from_user.first_name, last_name=msg.from_user.last_name, user_id=msg.from_user.id, mention=msg.from_user.mention)),
            reply_markup=Translation.INFO_BUTTONS
        )
    elif msg.data == "refreshme":
        if config.UPDATES_CHANNEL:
            invite_link = await Client.create_chat_invite_link(int(config.UPDATES_CHANNEL))
            try:
                user = await Client.get_chat_member(int(config.UPDATES_CHANNEL), msg.from_user.id)
                if user.status == "kicked":
                    await msg.message.edit(
                        text="Sorry Sir, You are Banned to use me. Contact my [Support Group](https://t.me/leosupportx).",
                        parse_mode=enums.ParseMode.MARKDOWN,
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                await msg.message.edit(
                    text="<b>Hey</b> {},\n\n<b>You still didn't join our Updates Channel ☹️ \nPlease Join and hit on the 'Refresh 🔄' Button</b>".format(msg.from_user.mention),
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("Join Our Updates Channel 🗣", url=invite_link.invite_link)
                            ],
                            [
                                InlineKeyboardButton("Refresh 🔄", callback_data="refreshme")
                            ]
                        ]
                    ),
                    parse_mode=enums.ParseMode.HTML
                )
                return
            except Exception:
                await msg.message.edit(
                    text="Something went Wrong. Contact my [Support Group](https://t.me/leosupportx).",
                    parse_mode=enums.ParseMode.MARKDOWN,
                    disable_web_page_preview=True
                )
                return
        await msg.answer(f"Hey {msg.from_user.first_name} ,\n\nYou Got Access !!\n\nSend Me The Song Name In Correct Format To Download 🌝", show_alert=True)
        await msg.message.delete()
    else:
        await msg.message.delete()
