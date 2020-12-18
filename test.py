import datetime
import json
import os
import time

from crsbot_source import get_json, random_select, log

# get_json.official_test()
# print(get_json.is_json_not_exists_or_outdated("domestic"))
region = "domestic"
try:
    get_json.official(region)
except ValueError:
    log.logger(f"関数officialへの入力が不正です: '{region}'", "critical")
    # 内部でエラーを起こす
