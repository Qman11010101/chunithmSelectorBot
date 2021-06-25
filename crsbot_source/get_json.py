import json
import os
import time

import requests

from .consts import CHUNIREC_TOKEN, URL_MAIMAI, URL_ONGEKI, URL_chunirec
from .exceptions import TooManyRequestsError
from .log import logger


def is_json_not_exists_or_outdated(filename):
    logger(f"{filename}.jsonの新旧をチェックします")
    json_path = f"api_log/{filename}.json"
    exists = os.path.isfile(json_path)
    NOT_EXISTS = not exists
    OUTDATED = False
    if exists:
        if time.time() - os.path.getmtime(json_path) > 3600:
            logger(f"{filename}.jsonは古くなっています")
            OUTDATED = True
        else:
            logger(f"最新の{filename}.jsonが存在しています")
    else:
        logger(f"{filename}.jsonが存在していません")
    return NOT_EXISTS or OUTDATED

def save_and_return_json(url, filename):
    logger(f"{url}を{filename}.jsonとして取得します")
    # chunirecエンドポイント変更により不要になったコード
    # if filename == "chunirec":
    #     response = requests.get(f"{url}.json")
    #     if response.status_code == 429: # 動作する？
    #         logger("chunirecから429エラーを受け取りました", "error")
    #         raise TooManyRequestsError
    # else:
    #     response = requests.get(f"{url}.json")
    response = requests.get(f"{url}.json")
    data = response.json()
    with open(f"api_log/{filename}.json", "w", encoding="UTF-8_sig") as a:
        json.dump(data, a, ensure_ascii=False)
    return data

def chunirec():
    """chunirecからJSONファイルを取得し、辞書を返します。\n

    返り値:\n
        JSONデータ(dict): 全楽曲の情報が記載されている辞書データです。

    例外:\n
        TooManyRequestsError: リクエストの量が多すぎて429を返された際に発生します。
    """
    if is_json_not_exists_or_outdated("chunirec"):
        json_data = save_and_return_json(URL_chunirec, "chunirec")
    else:
        with open(f"api_log/chunirec.json", "r", encoding="UTF-8_sig") as a:
            json_data = json.load(a)

    return json_data

def official(game):
    """maimai/オンゲキの公式サイトからJSONファイルを取得し、辞書を返します。
    引数は『ongeki』『maimai』のどちらかです。"""
    if is_json_not_exists_or_outdated(f"{game}"):
        json_data = save_and_return_json(URL_ONGEKI.replace(".json", "") if game == "ongeki" else URL_MAIMAI.replace(".json", ""), game)
    else:
        with open(f"api_log/{game}.json", "r", encoding="UTF-8_sig") as a:
            json_data = json.load(a)

    return json_data
