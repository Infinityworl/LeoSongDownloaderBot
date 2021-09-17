# Leo Projects <https://t.me/leosupportx>

import os
from LeoSongDownloaderBot.plugins.heroku_updater import fetch_heroku_git_url

API_ID = int(os.getenv("API_ID", 2158704))
API_HASH = os.getenv("API_HASH", "227f3bd8c1d7fc3ecfa243e1a85dd2fa")
BOT_TOKEN = os.getenv("BOT_TOKEN", "1996816091:AAFDEHO2Cadmg9zpZ_rQ5cLK231Fy_koQgE")
UPDATES_CHANNEL = int(os.environ.get("UPDATES_CHANNEL", -1001231683570))
BOT_USERNAME = os.environ.get("BOT_USERNAME", "leosongdownloaderbot")
SESSION_NAME = os.environ.get("SESSION_NAME", "LeoSongDownloaderBot")
BOT_OWNER = int(os.environ.get("BOT_OWNER", 1069002447))
BROADCAST_AS_COPY = bool(os.environ.get("BROADCAST_AS_COPY", False))
MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb+srv://navindu:navi18572@cluster0.9yrur.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", -1001511224747))
ARQ_API_KEY = os.getenv("ARQ_API_KEY", "RZOGUI-VCYTJC-FBTHZH-KWCYGT-ARQ")

# Updator Configs
HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY")
UPSTREAM_REPO = os.environ.get("UPSTREAM_REPO", "https://github.com/Itz-fork/Callsmusic-Plus")
U_BRANCH = "devs"
HEROKU_URL = fetch_heroku_git_url(HEROKU_API_KEY, HEROKU_APP_NAME)


