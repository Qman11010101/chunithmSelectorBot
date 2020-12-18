import datetime
import json
import os
import sys

import pytz

if os.path.isfile("setting.json"):
    with open("setting.json") as s:
        setting = json.load(s)
    
    tz = setting["misc"]["timezone"]
    is_logging = setting["logging"]["logging"]
    loglevel = setting["logging"]["loglevel"]
else:
    logger("setting.jsonが見つかりませんでした", "critical")
    sys.exit(1)
    # TODO: 環境変数読むか起動時に引数もらう

TIMEZONE = pytz.timezone(tz)

def logger(content, level=loglevel):
    """ロギングを行います。

    引数:
        content(str): ログ出力する内容です。
        level(str) :ログレベルです。デフォルトはsetting.jsonで指定したものです。
                    任意のレベルが指定できますが、基本的には以下の5つのうちどれかを指定します。
                    - debug
                    - info
                    - warning
                    - error
                    - critical
    """
    now_str = TIMEZONE.localize(datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now_str}][{level}]: {content}")

if __name__ == "__main__":
    logger("ロギングテスト")