import os
import sys

import discord
from discord.ext import commands

import token_test
from crsbot_source import client
from crsbot_source.consts import CMDPREF, DISCORD_TOKEN
from crsbot_source.log import logger

if not os.path.isfile("setting.json"):
    print("エラー: setting.jsonが見つかりません")
    sys.exit(1)

logger("chunirec tokenのテストを行います", level="debug")
test_status = token_test.test_chunirec()
if test_status != 200:
    if test_status == 429:
        logger("chunirecにおいて、tokenのリクエスト過多により、一時的に使用できなくなっています", "critical")
    else:
        logger("chunirecのtokenが不正です", "critical")
    sys.exit(1)
logger("tokenは正しく設定されています", level="debug")

logger("APIから取得したファイルの保存ディレクトリを生成します", level="debug")
os.makedirs("api_log", exist_ok=True)

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(CMDPREF),
    help_command=None,
    case_insensitive=True,
    activity=discord.Game("CHUNITHM")
)
bot.add_cog(client.ChunithmSelector(bot))

logger("botを起動します", level="debug")
bot.run(DISCORD_TOKEN)
