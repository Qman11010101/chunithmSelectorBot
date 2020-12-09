import requests

URL_International = "https://chunithm.sega.com/js/music/json/common.json"
URL_Domestic = "https://chunithm.sega.jp/data/common.json"

def get_json(version):
    if version == "International":
        response = requests.get(URL_International)
    elif version == "Japan":
        response = requests.get(URL_Domestic)
    else:
        response = requests.get(URL_Domestic)
