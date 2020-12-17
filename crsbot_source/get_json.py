import json
import os
import datetime

import requests

URL_International = "https://chunithm.sega.com/js/music/json/common.json"
URL_Domestic = "https://chunithm.sega.jp/data/common.json"

def is_json_exists(region):
    return True if os.path.isfile(f"{region}.json") else False

def is_json_timeout(region):
    return True

def official(version):
    """公式サイトから取得されたJSONファイルを取得します。
    引数で日本版と国際版どちらを取得するか選ぶことができます。

    引数:
        version(str): "international"もしくは"domestic"の値のみを取り得ます。
                      前者で国際版、後者で日本版のJSONを取得することができます。
                      大文字が混じっていた場合、小文字に変換されます。
                      変換後、2つのどちらの値とも違う場合は、"domestic"の結果が返されます。
    """
    ver = version.lower()
    if is_json_exists and is_json_timeout:
        pass
    # if ver == "international":
    #     region = ver
    # elif ver == "domestic":
    #     region = ver
    # else:
    #     region = "domestic"

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
