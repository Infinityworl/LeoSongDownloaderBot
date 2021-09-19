import os
import time
import asyncio
import datetime
import pytz
from pyromod import listen
from LeoSongDownloaderBot.translation import Translation
import config
from LeoSongDownloaderBot.plugins.youtube import callback_query_ytdl_audio
from helper.database.access_db import db
from pyrogram import Client
from asyncio import TimeoutError
from pyrogram.errors import UserNotParticipant
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, Message, ForceReply
from LeoSongDownloaderBot import LeoSongDownloaderBot as app

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
            message_ids=msg.message.message_id
        )
        await msg.answer(f"{msg.from_user.first_name} ,Successfully Sent To Your PM 💫", show_alert=False)
    
    elif msg.data == "report_to_owner":
        await Client.forward_messages(
            from_chat_id=msg.message.chat.id,
            chat_id=-1001523985078, 
            message_ids=msg.message.message_id
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
            reply_to_message_id=msg.message.message_id,
            reply_markup=ForceReply()
        )
        try:
            ask_ : Message = await Client.listen(msg.message.chat.id, timeout=300)
            if ask_.text.startswith("-100"):
                pass
            else:
                await msg.message.reply_text(
                    text=f"<b>Sorry</b> {msg.from_user.mention} !\n\n <b>You Entered</b> <code>{ask_.text}</code> <b>Is Not Correct Group Id 😐</b>",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Retry 💫", callback_data="group")],[InlineKeyboardButton("Close ❌", callback_data="close")]]),
                    parse_mode="html"
                )
            if len(ask_.text) >= 13:
                pass
            else:
                missed_words = 13 - len(ask_.text)
                await msg.message.reply_text(
                    text=f"<b>Sorry</b> {msg.from_user.mention} !\n\n <b>You Entered</b> <code>{ask_.text}</code> <b>Is Not Correct Group Id 😐</b>\n\n<b>It Missed {missed_words} Words ❗</b>",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Retry 💫", callback_data="group")],[InlineKeyboardButton("Close ❌", callback_data="close")]]),
                    parse_mode="html"
                )
        except TimeoutError:
            await msg.answer(f"Sorry {msg.from_user.first_name}, Sorry Timed Out !!", show_alert=False)
        
        await Client.forward_messages(
            from_chat_id=msg.message.chat.id,
            chat_id=int(ask_.text), 
            message_ids=msg.message.message_id
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
            reply_to_message_id=msg.message.message_id,
            reply_markup=ForceReply()
        )
        try:
            ask_ : Message = await Client.listen(msg.message.chat.id, timeout=300)
            if ask_.text.startswith("-100"):
                pass
            else:
                await msg.message.reply_text(
                    text=f"<b>Sorry</b> {msg.from_user.mention} !\n\n <b>You Entered</b> <code>{ask_.text}</code> <b>Is Not Correct Channel Id 😐</b>",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Retry 💫", callback_data="channel")],[InlineKeyboardButton("Close ❌", callback_data="close")]]),
                    parse_mode="html"
                )
            if len(ask_.text) >= 13:
                pass
            else:
                missed_words = 13 - len(ask_.text)
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
            message_ids=msg.message.message_id
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
        await msg.answer(f"{msg.from_user.first_name},\nPlease use the below format to download songs from YouTube 😊\n\nFormat : /song song_name 💫", show_alert=True)
    
    elif msg.data == "help_for_saavn":
        await msg.answer(f"{msg.from_user.first_name},\nPlease use the below format to download song from Saavn 😊\n\nFormat : /saavn song_name 💫", show_alert=True)
    
    elif msg.data == "help_for_lyrics_down":
        await msg.answer(f"{msg.from_user.first_name},\nplease use the below format to download lyrics 😊\n\nFormat : /lyrics song_name 💫", show_alert=True)

    elif msg.data == "help_for_url_dl":
        await msg.answer(f"{msg.from_user.first_name},\n Simply copy an url from YT and Paste it on this bot 😊" , show_alert=True)
    
    elif msg.data == "bot_users_count":
        user_count = await db.total_users_count()
        dt = datetime.datetime.now(pytz.timezone("UTC")).strftime("%I:%M %p %d/%m/%y") 
        dtsl = datetime.datetime.now(pytz.timezone("Asia/Colombo")).strftime("%I:%M %p %d/%m/%y")
        await msg.answer(f"Hi {msg.from_user.first_name} 👋\n\nTotal Users : {user_count} 💫\n\nLast Update :\n {dt} (UTC 🌎)\n {dtsl} (Sri Lanka 🇱🇰)\n\nShare And Support Us 😊", show_alert=True)
    
    elif msg.data == "no":
        await msg.message.edit_text(text = f"{msg.from_user.mention},\n\nSorry For Disturbing You ☹️")
        await asyncio.sleep(2)
        await msg.message.delete()

    elif msg.data == "yes":
        await msg.message.edit_media(media=InputMediaPhoto("https://telegra.ph/file/7af5e5f9537e4bbe3461a.jpg", caption="This Help Menu Will Be Usefull To You 😊\n\nUse The Below Buttons To Know How To Download Songs With Me 😊"),
            reply_markup=Translation.HELP_BUTTONS
        )
        
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
                user = await Client.get_chat_member(int(config.UPDATES_CHANNEL), msg.message.chat.id)
                if user.status == "kicked":
                    await msg.message.edit(
                        text="Sorry Sir, You are Banned to use me. Contact my [Support Group](https://t.me/leosupportx).",
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                await msg.message.edit(
                    text="<b>Hey</b> {},\n\n<b>You still didn't join our Updates Channel ☹️ \nPlease Join and hit on the 'Refresh 🔄' Button</b>".format(message.from_user.mention),
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
                    parse_mode="HTML"
                )
                return
            except Exception:
                await msg.message.edit(
                    text="Something went Wrong. Contact my [Support Group](https://t.me/leosupportx).",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        await msg.message.edit(
            text=Translation.START_TEXT.format(msg.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=Translation.START_BUTTONS,
        )
    else:
        await msg.message.delete()
