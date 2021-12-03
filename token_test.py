import json
import os

import requests
from crsbot_source.log import logger

def test_chunirec():
    """chunirecのトークンが正しいかどうかテストします。\n
    返り値: \n
        HTTPステータスコード(int)
    """
    with open("setting.json", "r", encoding="UTF-8_sig") as s:
        s_json = json.load(s)
    p = {"token": s_json["token"]["chunirec"]} if os.path.isfile("setting.json") else {"token": os.environ["chunirec_token"]}
    r = requests.get("https://api.chunirec.net/2.0/users/me.json", params=p)
    return r.status_code


if __name__ == "__main__":
    logger("chunirecのtokenのテストを行います", "debug")
    status = test_chunirec()
    if status == 200:
        logger("tokenは正しく設定されています", "debug")
    else:
        logger("tokenが正しくないようです", "debug")
