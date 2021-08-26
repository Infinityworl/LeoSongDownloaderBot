import os
from LeoSongDownloaderBot.translation import Translation
import config
from LeoSongDownloaderBot.plugins.youtube import callback_query_ytdl_audio
from pyrogram import Client
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
from LeoSongDownloaderBot import LeoSongDownloaderBot as app



@app.on_callback_query()
async def cb_data(Client, msg:CallbackQuery):
    if msg.data == "home":
        await msg.message.edit_text(
            text=Translation.START_TEXT.format(msg.from_user.mention),
            reply_markup=Translation.START_BUTTONS,
            disable_web_page_preview=True,
        )
    elif msg.data == "help":
        await msg.message.edit_media(media=InputMediaPhoto("https://telegra.ph/file/7af5e5f9537e4bbe3461a.jpg", caption=""),
            reply_markup=Translation.HELP_BUTTONS,
        )
    elif msg.data == "help_for_yt":
        await msg.answer("Please use the below format to download songs from YouTube 😊\n\nFormat : /song song_name 💫", show_alert=True)
    
    elif msg.data == "help_for_saavn":
        await msg.answer("Please use the below format to download song from Saavn 😊\n\nFormat : /saavn song_name 💫", show_alert=True)
    
    elif msg.data == "help_for_lyrics_down":
        await msg.answer("please use the below format to download lyrics 😊\n\nFormat : /lyrics song_name 💫", show_alert=True)

    elif msg.data =="help_for_url_dl":
        await msg.answer("Simply copy an url from YT and Paste it on this bot 😊", show_alert=True)

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