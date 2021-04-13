import random
import textwrap
import traceback

import discord
from discord.ext import commands

from .consts import APP_VERSION, CHANNEL_NAME, CMDPREF, MAX_MUSICS
from .exceptions import TooManyRequestsError
from .log import logger
from .search import search_chunirec


def command_parser(command):
    cl = command.split()
    for e in range(len(cl)):
        if cl[e] == "-" or cl[e].lower() == "none":
            cl[e] = [None, None]
        elif ":" in cl[e]:
            e_temp = cl[e].split(":")
            if (ud_val := e_temp[1].lower()) in ("high", "up", "big", "huge"):
                ud_val = "high"
            elif ud_val in ("low", "down", "small", "tiny"):
                ud_val = "low"
            else:
                ud_val = None
            cl[e] = [e_temp[0], ud_val]
        else:
            cl[e] = [cl[e], None]
    while len(cl) < 7:
        cl.append([None, None])
    return cl

class ChunithmSelector(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def random(self, ctx, *, arg=""):
        if ctx.message.channel.name != CHANNEL_NAME:
            embed_mes = discord.Embed(title="Error", description=f"コマンドは『{CHANNEL_NAME}』チャンネルで実行してください。", color=0xff0000)
            await ctx.send(embed=embed_mes)
            return
        logger(f"{ctx.author.name}: {CMDPREF}random {arg}")
        if not arg:
            logger(f"引数が存在しないため、自動的に3曲選曲します", level="debug")
            arg = "3"
        c = command_parser(arg)
        try:
            music_count = c[0][0]
            # music_countを上限までに設定する
            if not music_count:
                music_count = 3
            music_count = min(int(music_count), MAX_MUSICS)
            logger(f"曲数を{music_count}曲に設定しました", level="debug")
            res = search_chunirec(level=c[1][0], level_range=c[1][1], category=c[2][0], artist=c[3][0], notes=c[4][0], notes_range=c[4][1], bpm=c[5][0], bpm_range=c[5][1], difficulty=c[6][0])
            r = random.sample(res, min(len(res), music_count))
            if (lr := len(r)) > 0:
                logger(f"以下の{lr}曲が選ばれました:")
                embed_mes = discord.Embed(title="選曲結果", description=f"以下の{lr}曲が選ばれました", color=0x00ff00)
                for m in r:
                    title = m["meta"]["title"]
                    artist = m["meta"]["artist"]
                    category = m["meta"]["genre"]
                    diff_e = m["data"]["EXP"]["const"]
                    diff_m = m["data"]["MAS"]["const"]
                    bpm = m["meta"]["bpm"]
                    notes_e = m["data"]["EXP"]["maxcombo"]
                    notes_m = m["data"]["MAS"]["maxcombo"]
                    embed_mes.add_field(name=title, value=f"**ARTIST**: {artist}\n**GENRE**: {category}\n**CONST** EXP: {float(diff_e)} / MAS: {float(diff_m)}\n**BPM**: {bpm}\n**NOTES** EXP: {notes_e} / MAS: {notes_m}", inline=False)
                    logger(f"・『{title}』")
            else:
                logger(f"条件に合致する楽曲はありませんでした")
                embed_mes = discord.Embed(title="Unfound", description="条件に合致する楽曲が見つかりませんでした。", color=0x0000ff)
        except TooManyRequestsError:
            embed_mes = discord.Embed(title="Error", description="一時的にリクエスト過多になっています。10分ほど時間を置いて、再度お試しください。", color=0xff0000)
        except (TypeError, ValueError):
            embed_mes = discord.Embed(title="Error", description="パラメータの形式が正しくありません。もう一度確認してください。", color=0xff0000)
        except Exception as e:
            embed_mes = discord.Embed(title="Error", description="不明なエラーが発生しました。botの管理者に連絡してください。", color=0xff0000)
            logger("内部エラーが発生しました", level="error")
            logger(traceback.format_exc(), level="error")
        finally:
            await ctx.reply(embed=embed_mes)

    @commands.command()
    async def search(self, ctx, *, arg=""):
        if ctx.message.channel.name != CHANNEL_NAME:
            embed_mes = discord.Embed(title="Error", description=f"コマンドは『{CHANNEL_NAME}』チャンネルで実行してください。", color=0xff0000)
            await ctx.send(embed=embed_mes)
            return
        if not arg:
            await ctx.send(discord.Embed(title="Error", description="検索条件が指定されていません。"))
            return
        c = command_parser(arg)
        try:
            res = search_chunirec(level=c[0][0], level_range=c[0][1], category=c[1][0], artist=c[2][0], notes=c[3][0], notes_range=c[3][1], bpm=c[4][0], bpm_range=c[4][1], difficulty=c[5][0])
            if (lr := len(res)) > MAX_MUSICS:
                embed_mes = discord.Embed(title="Error", description=f"見つかった楽曲数({lr}曲)が{MAX_MUSICS}曲を超えるため、表示できません。", color=0xff0000)
            elif lr > 0:
                logger(f"以下の{lr}曲が見つかりました:")
                embed_mes = discord.Embed(title="検索結果", description=f"{lr}曲見つかりました。", color=0x00ff00)
                for m in res:
                    title = m["meta"]["title"]
                    artist = m["meta"]["artist"]
                    category = m["meta"]["genre"]
                    diff_e = m["data"]["EXP"]["const"]
                    diff_m = m["data"]["MAS"]["const"]
                    bpm = m["meta"]["bpm"]
                    notes_e = m["data"]["EXP"]["maxcombo"]
                    notes_m = m["data"]["MAS"]["maxcombo"]
                    embed_mes.add_field(name=title, value=f"**ARTIST**: {artist}\n**GENRE**: {category}\n**CONST** EXP: {float(diff_e)} / MAS: {float(diff_m)}\n**BPM**: {bpm}\n**NOTES** EXP: {notes_e} / MAS: {notes_m}", inline=False)
                    logger(f"・『{title}』")
            else:
                embed_mes = discord.Embed(title="Unfound", description="条件に合致する楽曲が見つかりませんでした。", color=0x0000ff)
        except TooManyRequestsError:
            embed_mes = discord.Embed(title="Error", description="一時的にリクエスト過多になっています。10分ほど時間を置いて、再度お試しください。", color=0xff0000)
        except (TypeError, ValueError):
            embed_mes = discord.Embed(title="Error", description="パラメータの形式が正しくありません。もう一度確認してください。", color=0xff0000)
        except Exception as e:
            embed_mes = discord.Embed(title="Error", description="不明なエラーが発生しました。botの管理者に連絡してください。", color=0xff0000)
            logger(traceback.format_exc(), level="error")
        finally:
            await ctx.reply(embed=embed_mes)

    @commands.command()
    async def help(self, ctx):
        if ctx.message.channel.name != CHANNEL_NAME:
            embed_mes = discord.Embed(title="Error", description=f"コマンドは『{CHANNEL_NAME}』チャンネルで実行してください。", color=0xff0000)
            await ctx.send(embed=embed_mes)
            return
        helpmes = textwrap.dedent(f"""
        **CHUNITHM Random Selector bot v{APP_VERSION}** by キューマン・エノビクト

        【コマンド文字列】
        `{CMDPREF}random [曲数] [レベル(:high/low)] [ジャンル] [アーティスト] [ノーツ数(:high/low)] [BPM(:high/low)] [難易度]`
        `{CMDPREF}search [レベル(:high/low)] [ジャンル] [アーティスト] [ノーツ数(:high/low)] [BPM(:high/low)] [難易度]`
        ※`(:high/low)`がついているパラメータは、後ろに『:high』もしくは『:low』を付け足すことで『以上』『以下』を表すことができます。

        【パラメータ】
        指定しないパラメータは、`-`もしくは`none`と入力してください。

        **曲数**
        > 表示する曲数を指定します。最大{MAX_MUSICS}曲まで表示できます。
        > それ以上の数字を入力した場合、ランダム選曲コマンドにおいては{MAX_MUSICS}曲として扱われ、検索コマンドではエラー扱いになります。
        > 指定されなかった場合、3曲として扱われます。
        > 半角数字で入力してください。

        **レベル**
        >  楽曲のレベルを指定します。
        > 『10』『13+』のような形で入力してください。

        **ジャンル**
        > 楽曲が属するジャンルを指定します。
        > 『ORIGINAL』『POPS&ANIME』『niconico』『東方Project』『VARIETY』『イロドリミドリ』『ゲキマイ』から1つ選んで入力してください。

        **アーティスト**
        > 楽曲のアーティスト名を指定します。
        > アーティスト名を入力してください。
        > 検索は大文字・小文字を考慮しない部分一致で検索されます。

        **ノーツ数**
        > 楽曲のノーツ数を指定します。
        > 半角数字で入力してください。

        **BPM**
        > 楽曲のBPMを指定します。
        > 半角数字で入力してください。

        **難易度**
        > 楽曲の難易度を指定します。EXPERTのみもしくはMASTERのみの検索をする場合に使用します。
        > 指定する場合、『exp』もしくは『mas』と指定してください。
        > 指定されないか、不正な値を指定した場合は自動的にEXPERTとMASTERの両方から検索します。
        > レベルもしくはノーツ数が指定されたときのみ機能します。

        【コマンド例】
        `{CMDPREF}random`: 全楽曲の中からランダムに3曲選びます。
        `{CMDPREF}random 5 13+:up`: レベル13+以上の楽曲の中からランダムに5曲選びます。
        `{CMDPREF}random - 13 - - - - exp`: レベル13のEXPERTの楽曲をランダムに3曲選びます。
        `{CMDPREF}search none 東方Project none 1000:low`: 東方Projectの楽曲の中からノーツ数が1000以下の楽曲を検索します。
        `{CMDPREF}search - - - - 300:high`: 全楽曲の中からBPM300以上の楽曲を検索します。

        【注意点】
        - ジャンルは1つのみ指定可能です。
        - 英数字は全角だと認識できません。
        - WORLD'S ENDには対応していません。
        - 一部の譜面定数が『0.0』と出力される場合があります。
        """)
        await ctx.send(helpmes)

class maimaiSelector(commands.Cog):
    pass

class OngekiSelector(commands.Cog):
    pass
