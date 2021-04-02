import random

from .consts import MAX_MUSICS
from .get_json import chunirec, official


def random_select(
        music_count=3,
        difficulty=None,
        difficulty_range=None,
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
        difficulty(str): 難易度を指定します。"12"や"13+"などの文字列で指定します。
        difficulty_range(str): 難易度の範囲を指定します。"high"または"low"を指定します。
        category(str): カテゴリを指定します。
        artist(str): アーティストを指定します。
        notes(int): ノーツ数を指定します。
        notes_range(str): ノーツ数の範囲を指定します。"high"または"low"を指定します。
        bpm(int): BPMを指定します。
        bpm_range(str): BPMの範囲を指定します。"high"または"low"を指定します。
    """
    # "n+"を"n.5"に変更し数値化
    if difficulty:
        difficulty = float(difficulty.replace("+", ".5"))

    # music_countを上限までに設定する
    music_count = min(music_count, MAX_MUSICS)

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

    return random.sample(temp_list, min(len(temp_list), music_count))

def random_select_international(
        music_count=3,
        difficulty=None,
        difficulty_range=None,
        category=None,
        artist=None):
    """指定された曲数分ランダムに選曲し、辞書形式で返します。\n
    MASTER以外の難易度は対象外です。

    引数:\n
        music_count(int): 曲数を指定します。デフォルトは3です。上限は20です。
        difficulty(str): 難易度を指定します。"12"や"13+"などの文字列で指定します。
        difficulty_range(str): 難易度の範囲を指定します。"high"または"low"を指定します。
        category(str): カテゴリを指定します。json内の"catcode"ではなく"category"の形式に従ってください。
        artist(str): アーティストを指定します。
    """
    # "n+"を"n.5"に変更し数値化
    if difficulty:
        difficulty = float(difficulty.replace("+", ".5"))

    music_json = official("international")
    temp_list = []

    for music in music_json:
        # 1つ1つの要素に対して判定をしていき、Falseが出た時点でcontinueして次へ行く
        # 全部通ったらtemp_listにappendする

        # WE除外
        if music["category"] == "worlds_end":  # 実際に実装されて違ったら書き直す
            continue

        # 難易度
        if difficulty:
            music_difficulty = float(music["lev_mas"].replace("+", ".5"))
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
            if music["category"] != category:  # categoryの方が扱いやすいのでそっちにする
                continue

        # アーティスト
        if artist:
            if music["artist"] != artist:
                continue

        temp_list.append(music)

    return random.sample(temp_list, min(len(temp_list), music_count))
