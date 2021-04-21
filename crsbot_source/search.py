from .consts import MAX_MUSICS
from .get_json import chunirec
from .log import logger


def is_value_invalid(factor, music_factor, factor_range):
    if music_factor == None:
        return True
    if factor_range: # 範囲指定
        if factor_range == "high":
            return True if factor > music_factor else False
        else:
            return True if factor < music_factor else False
    else: # 単一指定
        return True if music_factor != factor else False

def search_chunirec(
        level=None,
        level_range=None,
        category=None,
        artist=None,
        notes=None,
        notes_range=None,
        bpm=None,
        bpm_range=None,
        difficulty="default"):
    """指定された条件に合致する楽曲のリストを返します。\n
    上限はsettingで定められた数です。

    引数:\n
        level(str): レベルを指定します。"12"や"13+"などの文字列で指定します。
        level_range(str): レベルの範囲を指定します。"high"または"low"を指定します。
        category(str): カテゴリを指定します。
        artist(str): アーティストを指定します。
        notes(int): ノーツ数を指定します。
        notes_range(str): ノーツ数の範囲を指定します。"high"または"low"を指定します。
        bpm(int): BPMを指定します。
        bpm_range(str): BPMの範囲を指定します。"high"または"low"を指定します。
        difficulty(str): 難易度を指定します。"e"(EXPERT)/"m"(MASTER)/"b"(両方)のいずれかを指定します。
    """
    # "n+"を"n.5"に変更し数値化
    logger(f"レベル指定: {level}", level="debug")
    if level:
        level = float(level.replace("+", ".5"))

    music_json = chunirec()
    temp_list = []

    # 難易度をバリデーション
    if difficulty:
        if difficulty[0].lower() not in ("e", "m", "b"):
            difficulty = "b"
        else:
            difficulty = difficulty[0].lower()
    else:
        difficulty = "b" # TODO: もうちょいまともな実装にする

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

        # レベル
        if level:
            music_level_mas = music["data"]["MAS"]["level"] if difficulty in ("b", "m") else None
            music_level_exp = music["data"]["EXP"]["level"] if difficulty in ("b", "e") else None
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
            music_notes_mas = music["data"]["MAS"]["maxcombo"] if difficulty in ("b", "m") else None
            music_notes_exp = music["data"]["EXP"]["maxcombo"] if difficulty in ("b", "e") else None
            if is_value_invalid(notes, music_notes_mas, notes_range) and is_value_invalid(notes, music_notes_exp, notes_range):
                continue

        # BPM
        if bpm:
            music_bpm = music["meta"]["bpm"]
            if is_value_invalid(bpm, music_bpm, bpm_range):
                continue

        temp_list.append(music)

    return temp_list

# もう使わないが、オンゲキの検索に応用できるかも
# def search_international(
#         level=None,
#         level_range=None,
#         category=None,
#         artist=None,
#         difficulty="default"):
#     # "n+"を"n.5"に変更し数値化
#     logger(f"レベル指定: {level}", level="debug")
#     if level:
#         level = float(level.replace("+", ".5"))

#     music_json = official("international")
#     temp_list = []

#     # 難易度をバリデーション
#     if difficulty:
#         if difficulty[0].lower() not in ("e", "m", "b"):
#             difficulty = "b"
#     else:
#         difficulty = "b" # TODO: もうちょいまともな実装にする

#     for music in music_json:
#         # 1つ1つの要素に対して判定をしていき、Falseが出た時点でcontinueして次へ行く
#         # 全部通ったらtemp_listにappendする

#         # WE除外
#         if music["category"] == "worlds_end":  # 実際に実装されて違ったら書き直す
#             continue

#         # レベル
#         if level:
#             music_level_mas = float(music["lev_mas"].replace("+", ".5")) if difficulty in ("b", "m") else None
#             music_level_exp = float(music["lev_exp"].replace("+", ".5")) if difficulty in ("b", "e") else None
#             if is_value_invalid(level, music_level_mas, level_range) and is_value_invalid(level, music_level_exp, level_range):
#                 continue

#         # カテゴリ
#         if category:
#             if music["category"] != category:  # categoryの方が扱いやすいのでそっちにする
#                 continue

#         # アーティスト
#         if artist:
#             if music["artist"] != artist:
#                 continue

#         temp_list.append(music)

#     return temp_list
