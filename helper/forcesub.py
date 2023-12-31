# © Naviya2

import asyncio
import config
from pyrogram import Client, enums
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message


async def ForceSub(bot: Client, event: Message):
    """
    Custom Pyrogram Based Telegram Bot's Force Subscribe Function by @Naviya2.
    If User is not Joined Force Sub Channel Bot to Send a Message & ask him to Join First.
    
    :param bot: Pass Client.
    :param event: Pass Message.
    :return: It will return 200 if Successfully Got User in Force Sub Channel and 400 if Found that User Not Participant in Force Sub Channel or User is Kicked from Force Sub Channel it will return 400. Also it returns 200 if Unable to Find Channel.
    """
    
    try:
        invite_link = await bot.create_chat_invite_link(chat_id=(int(config.UPDATES_CHANNEL)))
    except FloodWait as e:
        await asyncio.sleep(e.x)
        fix_ = await ForceSub(bot, event)
        return fix_
    except Exception as err:
        print(f"Unable to do Force Subscribe to {config.UPDATES_CHANNEL}\n\nError: {err}\n\nContact Support Group: https://t.me/leosupportx")
        return 200
    try:
        user = await bot.get_chat_member(chat_id=(int(config.UPDATES_CHANNEL)), user_id=event.from_user.id)
        if user.status == "kicked":
            await bot.send_message(
                chat_id=event.from_user.id,
                text="Sorry Dear, You are Banned to use me ☹️\nFeel free to say in our [Support Group](https://t.me/leosupportx).",
                parse_mode=enums.ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_to_message_id=event.id
            )
            return 400
        else:
            return 200
    except UserNotParticipant:
        await event.reply_text(
            text="<b>Hello {} 👋\n\nYou Can't Download Songs From Me Until Subscribe Our Updates Channel ☹️\n\nSo Please join our Updates Channel by the following button and hit on the 'Refresh 🔄' Button 😊</b>".format(event.from_user.mention),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Join Our Updates Channel 🗣", url=invite_link.invite_link)
                    ],

                    [   
                        InlineKeyboardButton("Refresh 🔄", callback_data="refreshme")
                    ],
                ]
            ),
            parse_mode=enums.ParseMode.HTML,
            reply_to_message_id=event.id
        )
        return 400
    except FloodWait as e:
        await asyncio.sleep(e.x)
        fix_ = await ForceSub(bot, event)
        return fix_
    except Exception as err:
        print(f"Something Went Wrong! Unable to do Force Subscribe.\nError: {err}\n\nContact Support Group: https://t.me/leosupportx")
        return 200
