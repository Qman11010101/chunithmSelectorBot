import random
import json

from .log import logger
from .get_json import official, chunirec
from .exceptions import TooManyRequestsError

def random_select(music_number=3, difficulty=None, difficulty_range=None, category=None, artist=None, notes=None, notes_range=None):
    """指定された曲数分ランダムに選曲し、辞書形式で返します。\n
    WORLD'S ENDおよびMASTER以外の難易度は対象外です。
    
    引数:\n
        music_number(int): 曲数を指定します。デフォルトは3です。上限は20です。
        difficulty(str): 難易度を指定します。"12"や"13+"などの文字列で指定します。
        difficulty_range(str): 難易度の範囲を指定します。"high"または"low"を指定します。
        category(str): カテゴリを指定します。
        artist(str): アーティストを指定します。
        notes(int): ノーツ数を指定します。
        notes_range(str): ノーツ数の範囲を指定します。"high"または"low"を指定します。
    
    例外:\n
        TooManyRequestsError: リクエストの量が多すぎて429を返された際に発生します。
    """
    # "n+"を"n.5"に変更し数値化
    if difficulty:
        difficulty = float(difficulty.replace("+", ".5"))

    try:
        music_json = chunirec()
    except TooManyRequestsError:
        raise TooManyRequestsError
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
            if difficulty_range: # 範囲指定
                if difficulty_range == "high":
                    if difficulty > music_difficulty:
                        continue
                else:
                    if difficulty < music_difficulty:
                        continue
            else: # 単一指定
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
            if notes_range: # 範囲指定
                if notes_range == "high":
                    if notes > music_notes:
                        continue
                else:
                    if notes < music_notes:
                        continue
            else: # 単一指定
                if music_notes != notes:
                    continue
        
        temp_list.append(music)

    return random.sample(temp_list, min(len(temp_list), music_number))

def random_select_international(music_number=3, difficulty=None, difficulty_range=None, category=None, artist=None):
    """指定された曲数分ランダムに選曲し、辞書形式で返します。\n
    MASTER以外の難易度は対象外です。
    
    引数:\n
        music_number(int): 曲数を指定します。デフォルトは3です。上限は20です。
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
        if music["category"] == "worlds_end": # 実際に実装されて違ったら書き直す
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
            if music["category"] != category: # categoryの方が扱いやすいのでそっちにする
                continue

        # アーティスト
        if artist:
            if music["artist"] != artist:
                continue
    
        temp_list.append(music)
    
    return random.sample(temp_list, min(len(temp_list), music_number))
