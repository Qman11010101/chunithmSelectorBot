import random

from .consts import MAX_MUSICS
from .get_json import chunirec, official
from .log import logger


def is_value_invalid(factor, music_factor, factor_range):
    if factor_range: # 範囲指定
        if factor_range == "high":
            return True if factor > music_factor else False
        else:
            return True if factor < music_factor else False
    else: # 単一指定
        return True if music_factor != factor else False

def random_select(
        music_count=None,
        level=None,
        level_range=None,
        category=None,
        artist=None,
        notes=None,
        notes_range=None,
        bpm=None,
        bpm_range=None):
    """指定された曲数分ランダムに選曲し、辞書形式で返します。\n
    WORLD'S ENDおよびMASTER以外の難易度は対象外です。

    引数:\n
        music_count(int): 曲数を指定します。デフォルトは3です。上限は20です。
        level(str): 難易度を指定します。"12"や"13+"などの文字列で指定します。
        level_range(str): 難易度の範囲を指定します。"high"または"low"を指定します。
        category(str): カテゴリを指定します。
        artist(str): アーティストを指定します。
        notes(int): ノーツ数を指定します。
        notes_range(str): ノーツ数の範囲を指定します。"high"または"low"を指定します。
        bpm(int): BPMを指定します。
        bpm_range(str): BPMの範囲を指定します。"high"または"low"を指定します。
    """
    # "n+"を"n.5"に変更し数値化
    logger(f"難易度指定: {level}", level="debug")
    if level:
        level = float(level.replace("+", ".5"))
    # music_countを上限までに設定する
    if not music_count:
        music_count = 3
    music_count = min(int(music_count), MAX_MUSICS)
    logger(f"曲数を{music_count}曲に設定しました", level="debug")

    music_json = chunirec()
    temp_list = []

    # 変数の型を変えておく
    if notes:
        notes = int(notes)
    if bpm:
        bpm = int(bpm)

    for music in music_json:
        # 1つ1つの要素に対して判定をしていき、Falseが出た時点でcontinueして次へ行く
        # 全部通ったらtemp_listにappendする

        # WE除外
        if music["meta"]["genre"] == "WORLD'S END":
            continue

        # 難易度
        if level:
            music_level_mas = music["data"]["MAS"]["level"]
            music_level_exp = music["data"]["EXP"]["level"]
            if is_value_invalid(level, music_level_mas, level_range) and is_value_invalid(level, music_level_exp, level_range):
                continue

        # カテゴリ
        if category:
            if not category.lower() in music["meta"]["genre"].lower():
                continue

        # アーティスト
        if artist:
            if not artist.lower() in music["meta"]["artist"].lower():
                continue

        # ノーツ数
        if notes:
            music_notes_mas = music["data"]["MAS"]["maxcombo"]
            music_notes_exp = music["data"]["EXP"]["maxcombo"]
            if is_value_invalid(notes, music_notes_mas, notes_range) and is_value_invalid(notes, music_notes_exp, notes_range):
                continue

        # BPM
        if bpm:
            music_bpm = music["meta"]["bpm"]
            if is_value_invalid(bpm, music_bpm, bpm_range):
                continue

        temp_list.append(music)

    return random.sample(temp_list, min(len(temp_list), music_count))

def random_select_international(
        music_count=3,
        level=None,
        level_range=None,
        category=None,
        artist=None):
    """指定された曲数分ランダムに選曲し、辞書形式で返します。\n
    MASTER以外の難易度は対象外です。

    引数:\n
        music_count(int): 曲数を指定します。デフォルトは3です。上限は20です。
        level(str): 難易度を指定します。"12"や"13+"などの文字列で指定します。
        level_range(str): 難易度の範囲を指定します。"high"または"low"を指定します。
        category(str): カテゴリを指定します。json内の"catcode"ではなく"category"の形式に従ってください。
        artist(str): アーティストを指定します。
    """
    # "n+"を"n.5"に変更し数値化
    logger(f"難易度指定: {level}", level="debug")
    if level:
        level = float(level.replace("+", ".5"))
    # music_countを上限までに設定する
    if not music_count:
        music_count = 3
    music_count = min(int(music_count), MAX_MUSICS)
    logger(f"曲数を{music_count}曲に設定しました", level="debug")

    music_json = official("international")
    temp_list = []

    for music in music_json:
        # 1つ1つの要素に対して判定をしていき、Falseが出た時点でcontinueして次へ行く
        # 全部通ったらtemp_listにappendする

        # WE除外
        if music["category"] == "worlds_end":  # 実際に実装されて違ったら書き直す
            continue

        # 難易度
        if level:
            music_level_mas = float(music["lev_mas"].replace("+", ".5"))
            music_level_exp = float(music["lev_exp"].replace("+", ".5"))
            if is_value_invalid(level, music_level_mas, level_range) and is_value_invalid(level, music_level_exp, level_range):
                continue

        # カテゴリ
        if category:
            if music["category"] != category:  # categoryの方が扱いやすいのでそっちにする
                continue

        # アーティスト
        if artist:
            if music["artist"] != artist:
                continue

        temp_list.append(music)

    return random.sample(temp_list, min(len(temp_list), music_count))
