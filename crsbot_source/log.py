import datetime
import json
import os
import sys

import pytz

with open("setting.json") as s:
    setting = json.load(s)

tz = setting["misc"]["timezone"]
is_logging = setting["logging"]["logging"]
loglevel = setting["logging"]["loglevel"]

TIMEZONE = pytz.timezone(tz)
loglv_list = {
    "debug": 0,
    "info": 1,
    "warning": 2,
    "error": 3,
    "critical": 4
}

def logger(content, level=loglevel):
    """ロギングを行います。\n
    \n
    引数:\n
        content(str): ログ出力する内容です。
        level(str) :ログレベルです。デフォルトはsetting.jsonで指定したものです。
                    以下の5つのうちどれかを指定します。
                    - debug
                    - info
                    - warning
                    - error
                    - critical
                    存在しないレベルを指定した場合、自動的にinfoになります。
    """

    if level not in ["debug", "info", "warning", "error", "critical"]:
        level = "info"
    level_int = loglv_list[level]
    now_str = TIMEZONE.localize(datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now_str}][{level}]: {content}")

if __name__ == "__main__":
    logger("ロギングテスト", "debug")
