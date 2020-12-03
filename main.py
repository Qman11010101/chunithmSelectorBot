import json

import requests

# TODO: 公式かviewerかそれともchunirecか使う方を決める
music_data = requests.get("https://chuniviewer.net/GetMusicData.php").json()
print(music_data["150"]["name"])
# with open("music_list.json", "w", encoding="utf-8_sig") as f:
#     json.dump(music_data, f)
