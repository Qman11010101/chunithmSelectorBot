import datetime
import json
import os
import time

import requests

from .log import logger
from .exceptions import TooManyRequestsError
from .consts import URL_Domestic, URL_International, URL_chunirec, CHUNIREC_TOKEN, API_LIFETIME

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
        if response.status_code == 429:
            raise TooManyRequestsError
    else:
        response = requests.get(url)
    data = response.json()
    with open(f"api_log/{filename}.json", "w", encoding="UTF-8_sig") as a:
        json.dump(data, a, ensure_ascii=False)
    return data

def official(region):
    """公式サイトからJSONファイルを取得し、辞書を返します。\n
    引数で日本版と国際版どちらを取得するか選ぶことができます。

    引数:\n
        region(str): "international"もしくは"domestic"の値のみを取り得ます。
                      前者で国際版、後者で日本版のJSONを取得することができます。
                      大文字が混じっていた場合、小文字に変換されます。
                      どちらでもない値を指定した場合、ValueErrorを発生させます。
    
    返り値:\n
        JSONデータ(dict): 全楽曲の情報が記載されている辞書データです。

    例外:\n
        ValueError: 引数regionに指定された値が"international"または"domestic"のどちらでもなかった場合に発生します。
    """
    region = region.lower()
    if region not in ["domestic", "international"]:
        raise ValueError("Specified value is neither 'domestic' nor 'international'")
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
    """chunirecからJSONファイルを取得し、辞書を返します。\n

    返り値:\n
        JSONデータ(dict): 全楽曲の情報が記載されている辞書データです。

    例外:\n
        TooManyRequestsError: リクエストの量が多すぎて429を返された際に発生します。
    """
    if is_json_not_exists_or_outdated("chunirec"):
        logger(f"{URL_chunirec}をchunirec.jsonとして取得します")
        try:
            json_data = save_and_return_json(URL_chunirec, "chunirec", token=CHUNIREC_TOKEN)
        except TooManyRequestsError:
            raise TooManyRequestsError
    else:
        logger(f"新しいchunirec.jsonが存在しています")
        with open(f"api_log/chunirec.json", "r", encoding="UTF-8_sig") as a:
            json_data = json.load(a)
    
    return json_data
