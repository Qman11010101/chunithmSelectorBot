import requests

def get_json(version):
    if version == "International":
        response = requests.get("https://chunithm.sega.com/js/music/json/common.json")
    elif version == "Japan":
        response = requests.get("https://chunithm.sega.jp/data/common.json")
    else:
        response = requests.get("https://chunithm.sega.jp/data/common.json")
