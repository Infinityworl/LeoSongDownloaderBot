from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class Translation(object):


    START_TEXT = """
Hello {} 👋

I'm Leo Song Downloader Bot 🇱🇰

You can download any song within a shortime with this Bot 🙂

If you want to know how to use this bot just
touch on " Help 🆘 "  Button 😊
"""    

    ABOUT_TEXT = """
🔰 **Bot :** [Leo Song Downloader Bot 🇱🇰](https://t.me/leosongdownloaderbot)
🔰 **Developer :** [Naviya 🇱🇰](https://telegram.me/naviya2)
🔰 **Updates Channel :** [Leo Updates 🇱🇰](https://telegram.me/new_ehi)
🔰 **Support Group :** [Leo Support 🇱🇰](https://telegram.me/leosupportx)
🔰 **Language :** [Python3](https://python.org)
🔰 **Library :** [Pyrogram v1.2.0](https://pyrogram.org)
🔰 **Server :** [VPS](https://www.digitalocean.com)
"""

    INFO_TEXT = """
Hey {mention},

Your details are here 😊

🔰 **First Name :** `{first_name}`
🔰 **Last Name  :** `{last_name}`
🔰 **Username   :** @{username}
🔰 **User Id    :** `{user_id}`
"""

    START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Developer🧑‍💻', url='https://telegram.me/naviya2'),
        InlineKeyboardButton('Rate us ★', url='https://t.me/tlgrmcbot?start=leosongdownloaderbot-review')
        ],[
        InlineKeyboardButton('Updates Channel🗣', url='https://t.me/new_ehi'),
        InlineKeyboardButton('Support Group 👥', url='https://t.me/leosupportx')
        ],[
        InlineKeyboardButton('Help 🆘', callback_data='help')
        ],[
        InlineKeyboardButton('➕ Add me to your group ➕', url='t.me/leosongdownloaderbot?startgroup=true')
        ]]
    )
    HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Help For Download Songs From YT 🆘', callback_data='help_for_yt')
        ],[
        InlineKeyboardButton('Help For Download Songs From Saavn 🆘', callback_data='help_for_saavn')
        ],[
        InlineKeyboardButton('Help For Download Songs From YT URLs 🆘', callback_data='help_for_url_dl')
        ],[
        InlineKeyboardButton('Help For Download Lyrics 🆘', callback_data='help_for_lyrics_down')
        ],[
        InlineKeyboardButton('About ❗️', callback_data='about')
        ],[
        InlineKeyboardButton('Close ❎', callback_data='close')   
        ]]
    )
    ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('About Bot 🤖', callback_data='about_bot')
        ],[
        InlineKeyboardButton('About Dev 🧑‍💻', callback_data='aboutdev')
        ],[
        InlineKeyboardButton('About You ❗️', callback_data='user_info')
        ],[
        InlineKeyboardButton('Help 🆘', callback_data='help')
        ],[
        InlineKeyboardButton('Close ❎', callback_data='close')
        ]]
    )
    INFO_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Back 🔙', callback_data='about')
        ]]
    )
    ABOUT_BOT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Back 🔙', callback_data='about')
        ]]
    )
    ABOUT_DEV_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('About Him 💫', callback_data='aboutdevtext')
        ],[
        InlineKeyboardButton('Github', url='https://github.com/Naviya2')
        ],[
        InlineKeyboardButton('Telegram', url='https://t.me/naviya2')
        ],[
        InlineKeyboardButton('Back 🔙', callback_data='Back 🔙')
        ]]
    ) 