import datetime
import json
import os
import time

import requests

from .log import logger

URL_International = "https://chunithm.sega.com/js/music/json/common.json"
URL_Domestic = "https://chunithm.sega.jp/data/common.json"
URL_chunirec = "https://api.chunirec.net/1.3/music/showall.json"

with open("setting.json", "r", encoding="UTF-8_sig") as s:
    setting = json.load(s)

CHUNIREC_TOKEN = setting["token"]["chunirec"]
API_LIFETIME = int(setting["misc"]["api_lifetime"])

def is_json_not_exists_or_outdated(filename):
    json_path = f"api_log/{filename}.json"
    exists = os.path.isfile(json_path)
    NOT_EXISTS = not exists
    OUTDATED = False
    if exists:
        if time.time() - os.path.getmtime(json_path) > 3600:
            logger(f"{filename}.jsonは古くなっています")
            OUTDATED = True
    else:
        logger(f"{filename}.jsonが存在していません")
    return NOT_EXISTS or OUTDATED

def save_and_return_json(url, filename, token=None):
    if token:
        params = {"token": token}
        response = requests.get(url, params=params)
    else:
        response = requests.get(url)
    data = response.json()
    with open(f"api_log/{filename}.json", "w", encoding="UTF-8_sig") as a:
        json.dump(data, a, ensure_ascii=False)
    return data

def official(region):
    """公式サイトから取得されたJSONファイルを取得します。
    引数で日本版と国際版どちらを取得するか選ぶことができます。

    引数:
        region(str): "international"もしくは"domestic"の値のみを取り得ます。
                      前者で国際版、後者で日本版のJSONを取得することができます。
                      大文字が混じっていた場合、小文字に変換されます。
                      変換後、2つのどちらの値とも違う場合は、"domestic"の結果が返されます。
    """
    region = region.lower()
    if region not in ["domestic", "international"]:
        raise ValueError()
    if is_json_not_exists_or_outdated(region):
        if region == "international":
            url = URL_International
        else:
            url = URL_Domestic
        logger(f"{url}を{region}.jsonとして取得します")
        json_data = save_and_return_json(url, region)
    else:
        logger(f"新しい{region}.jsonが存在しています")
        with open(f"api_log/{region}.json", "r", encoding="UTF-8_sig") as a:
            json_data = json.load(a)
        
    return json_data

def chunirec():
    if is_json_not_exists_or_outdated("chunirec"):
        logger(f"{URL_chunirec}をchunirec.jsonとして取得します")
        json_data = save_and_return_json(URL_chunirec, "chunirec", token=CHUNIREC_TOKEN)
