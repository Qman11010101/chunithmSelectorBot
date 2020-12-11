import datetime
import json
import os
import sys

import pytz

if os.path.isfile("setting.json"):
    with open("setting.json") as s:
        setting = json.load(s)
    
    tz = setting["misc"]["timezone"]
else:
    print("setting.jsonが見つかりません")
    sys.exit(1)

TIMEZONE = pytz.timezone(tz)

def logger(content, mode="Info"):
    now = TIMEZONE.localize(datetime.datetime.now())
    print(now)

if __name__ == "__main__":
    logger("あ")