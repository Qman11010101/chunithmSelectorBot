import json

import requests

music_data = requests.get("https://chuniviewer.net/GetMusicData.php").json()
print(music_data["150"]["name"])
# with open("music_list.json", "w", encoding="utf-8_sig") as f:
#     json.dump(music_data, f)
