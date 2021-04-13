import json

with open("setting.json", "r", encoding="UTF-8_sig") as s:
    setting = json.load(s)

# URL
URL_International = "https://chunithm.sega.com/js/music/json/common.json"
URL_Domestic = "https://chunithm.sega.jp/data/common.json"
URL_chunirec = "https://api.chunirec.net/1.3/music/showall.json"

URL_ONGEKI = "https://ongeki.sega.jp/assets/json/music/music.json"
URL_MAIMAI = "https://maimai.sega.jp/data/DXsongs.json"

# トークン
CHUNIREC_TOKEN = setting["token"]["chunirec"]
DISCORD_TOKEN = setting["token"]["discord"]

# API関係
API_LIFETIME = int(setting["misc"]["api_lifetime"])

# logger関係
tz = setting["misc"]["timezone"]
is_logging = setting["logging"]["logging"]
loglevel_stdio = setting["logging"]["loglevel_stdio"]
loglevel_file = setting["logging"]["loglevel_file"]
log_filename = setting["logging"]["log_filename"]

# その他
MAX_MUSICS = setting["misc"]["max_musics"]
CMDPREF = setting["misc"]["command_prefix"]
APP_VERSION = "1.1.0β"
CHANNEL_NAME = "選曲bot"
