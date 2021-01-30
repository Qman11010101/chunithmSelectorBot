import json
import os
import sys

import discord
from discord.ext import commands
import requests

import token_test
from crsbot_source import client
from crsbot_source.log import logger
from crsbot_source.consts import DISCORD_TOKEN

if not os.path.isfile("setting.json"):
    print("エラー: setting.jsonが見つかりません")
    sys.exit(1)

logger("chunirec tokenのテストを行います", "debug")
test_status = token_test.test_chunirec()
if test_status != 200:
    if test_status == 429:
        logger("tokenのリクエスト過多により、一時的に使用できなくなっています", "critical")
    else:
        logger("tokenが不正です", "critical")
    sys.exit(1)
logger("tokenは正しく設定されています", "debug")

logger("APIより取得したファイルの保存ディレクトリを生成します", "debug")
os.makedirs("api_log", exist_ok=True)

client.client()
