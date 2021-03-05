from .consts import MAX_MUSICS
from .get_json import chunirec


def search_chunirec(
        music_number=3,
        difficulty=None,
        difficulty_range=None,
        category=None,
        artist=None,
        notes=None,
        notes_range=None,
        bpm=None,
        bpm_range=None):
    """指定された条件に合致する楽曲のリストを返します。\n
    上限はsettingで定められた数です。

    引数:\n
        music_number(int): 曲数を指定します。デフォルトは3です。上限は20です。
        difficulty(str): 難易度を指定します。"12"や"13+"などの文字列で指定します。
        difficulty_range(str): 難易度の範囲を指定します。"high"または"low"を指定します。
        category(str): カテゴリを指定します。
        artist(str): アーティストを指定します。
        notes(int): ノーツ数を指定します。
        notes_range(str): ノーツ数の範囲を指定します。"high"または"low"を指定します。
        bpm(int): BPMを指定します。
        bpm_range(str): BPMの範囲を指定します。"high"または"low"を指定します。

    例外:\n
        TooManyRequestsError: リクエストの量が多すぎて429を返された際に発生します。
    """

    music_json = chunirec()
    temp_list = []

    for music in music_json:
        # 1つ1つの要素に対して判定をしていき、Falseが出た時点でcontinueして次へ行く
        # 全部通ったらtemp_listにappendする

        # WE除外
        if music["meta"]["genre"] == "WORLD'S END":
            continue

        # 難易度
        if difficulty:
            music_difficulty = music["data"]["MAS"]["level"]
            if difficulty_range:  # 範囲指定
                if difficulty_range == "high":
                    if difficulty > music_difficulty:
                        continue
                else:
                    if difficulty < music_difficulty:
                        continue
            else:  # 単一指定
                if music_difficulty != difficulty:
                    continue

        # カテゴリ
        if category:
            if music["meta"]["genre"] != category:
                continue

        # アーティスト
        if artist:
            if music["meta"]["artist"] != artist:
                continue

        # ノーツ数
        if notes:
            music_notes = music["data"]["MAS"]["maxcombo"]
            if notes_range:  # 範囲指定
                if notes_range == "high":
                    if notes > music_notes:
                        continue
                else:
                    if notes < music_notes:
                        continue
            else:  # 単一指定
                if music_notes != notes:
                    continue

        # BPM
        if bpm:
            music_bpm = music["meta"]["bpm"]
            if bpm_range:  # 範囲指定
                if bpm_range == "high":
                    if bpm > music_bpm:
                        continue
                else:
                    if bpm < music_bpm:
                        continue
            else:  # 単一指定
                if music_bpm != bpm:
                    continue

        temp_list.append(music)
        if len(temp_list) == MAX_MUSICS:  # 最大曲数で切る
            break

    return temp_list


def search_international(
        difficulty=None,
        difficulty_range=None,
        category=None,
        artist=None):
    pass
