import os
import config
import sys
import heroku3
from functools import wraps
from os import environ, execle
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError
from pyrogram import Client, filters
from pyrogram.types import Message

REPO_ = UPSTREAM_REPO = "https://github.com/Naviya2/LeoSongDownloaderBot"
BRANCH_ = U_BRANCH = "devs"
HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY")

def fetch_heroku_git_url(api_key, app_name):
    if not api_key:
        return None
    if not app_name:
        return None
    heroku = heroku3.from_key(api_key)
    try:
        heroku_applications = heroku.apps()
    except:
        return None
    heroku_app = None
    for app in heroku_applications:
        if app.name == app_name:
            heroku_app = app
            break
    if not heroku_app:
        return None
    return heroku_app.git_url.replace("https://", "https://api:" + api_key + "@")

HEROKU_URL = fetch_heroku_git_url(HEROKU_API_KEY, HEROKU_APP_NAME)

heroku_client = None
if HEROKU_API_KEY:
    heroku_client = heroku3.from_key(HEROKU_API_KEY)

def _check_heroku(func):
    @wraps(func)
    async def heroku_cli(client, message):
        engine = message.Engine
        heroku_app = None
        if not heroku_client or not HEROKU_APP_NAME:
            await message.reply_text(
                message, engine.get_string("MISSING_API_KEY").format("HEROKU_API_KEY")
            )
        if HEROKU_APP_NAME and heroku_client:
            try:
                heroku_app = heroku_client.app(HEROKU_APP_NAME)
            except:
                await message.reply_text(
                    message, engine.get_string("HEROKU_DONT_MATCH")
                )
            if heroku_app:
                await func(client, message, heroku_app)

    return heroku_cli

@Client.on_message(filters.command("restart") & filters.user(1069002447))
@_check_heroku
async def gib_restart(client, message, hap):
    engine = message.Engine
    msg_ = await message.reply_text(message, engine.get_string("RESTART"))
    hap.restart()