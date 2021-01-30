import datetime

import pytz

from .consts import tz, log_filename, loglevel_file, loglevel_stdio, is_logging

TIMEZONE = pytz.timezone(tz)
loglv_list = {
    "debug": 0,
    "info": 1,
    "warning": 2,
    "error": 3,
    "critical": 4
}
log_stdio_int = loglv_list[loglevel_stdio]
log_file_int = loglv_list[loglevel_file]

def logger(content, level="info"):
    """ロギングを行います。\n
    標準出力とファイルへの出力
    \n
    引数:\n
        content(str): ログ出力する内容です。
        level(str) :ログレベルです。デフォルトはsetting.jsonで指定したものです。
                    以下の5つのうちどれかを指定します。
                    - debug
                    - info
                    - warning
                    - error
                    - critical
                    存在しないレベルを指定した場合、自動的にinfoになります。
    """

    if level not in ["debug", "info", "warning", "error", "critical"]:
        level = "info"
    level_int = loglv_list[level]

    now_str = TIMEZONE.localize(datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")

    log_content = f"[{now_str}][{level}]: {content}"

    # ログ(標準出力)
    if level_int >= log_stdio_int:
        print(log_content)
    
    # ログ(ファイル)
    if level_int >= log_file_int:
        with open(log_filename, "a", encoding="UTF-8_sig") as log:
            log.write(log_content + "\n")
