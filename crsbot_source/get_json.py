import datetime
import json
import os
import time

import requests

from .log import logger

URL_International = "https://chunithm.sega.com/js/music/json/common.json"
URL_Domestic = "https://chunithm.sega.jp/data/common.json"

def is_json_not_exists_or_outdated(filename):
    json_path = f"api_log/{filename}.json"
    os.makedirs("api_log", exist_ok=True)
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

def save_and_return_json(url, region):
    response = requests.get(url)
    data = response.json()
    with open(f"api_log/{region}.json", "w", encoding="UTF-8_sig") as a:
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

    

    # json_data = response.json()

    # with open(f"api_log/{region}.json", "w") as a:
    #     json.dump(json_data, a, ensure_ascii=False)
    # pass

def official_test():
    for i in [[URL_Domestic, "domestic"], [URL_International, "international"]]:
        response = requests.get(i[0])
        json_data = response.json()

        with open(f"api_log/{i[1]}.json", "w", encoding="utf-8_sig") as a:
            json.dump(json_data, a, ensure_ascii=False)
