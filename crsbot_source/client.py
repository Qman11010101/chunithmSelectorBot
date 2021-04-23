import random
import traceback

import discord
import jaconv
from discord.ext import commands

from .consts import CHANNEL_NAME, CMDPREF, HELPMES, MAX_MUSICS
from .exceptions import TooManyRequestsError
from .log import logger
from .search import search_chunirec


def command_parser(command):
    # 便宜上、各要素を長さ2のリストにしている
    # 「:high」「:low」のない要素のリストの2番目はNoneになる
    cl = jaconv.z2h(command, kana=False, digit=True, ascii=True).split()
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

def chunirec_parser(m, filler="未登録"):
    title = m["meta"]["title"]
    artist = m["meta"]["artist"]
    category = m["meta"]["genre"]
    diff_e = m["data"]["EXP"]["const"] if int(m["data"]["EXP"]["const"]) != 0 else filler
    diff_m = m["data"]["MAS"]["const"] if int(m["data"]["MAS"]["const"]) != 0 else filler
    bpm = m["meta"]["bpm"] if int(m["meta"]["bpm"]) != 0 else filler
    notes_e = m["data"]["EXP"]["maxcombo"] if int(m["data"]["EXP"]["maxcombo"]) != 0 else filler
    notes_m = m["data"]["MAS"]["maxcombo"] if int(m["data"]["MAS"]["maxcombo"]) != 0 else filler
    return [title, artist, category, diff_e, diff_m, bpm, notes_e, notes_m]

class ChunithmSelector(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def random(self, ctx, *, arg=""):
        if ctx.message.channel.name != CHANNEL_NAME:
            embed_mes = discord.Embed(title="Error", description=f"コマンドは『{CHANNEL_NAME}』チャンネルで実行してください。", color=0xff0000)
            await ctx.send(embed=embed_mes)
            return
        logger(f"【{ctx.guild.name}】{ctx.author.name}: {CMDPREF}random {arg}")
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
                    data = chunirec_parser(m)
                    title = data[0]
                    artist = data[1]
                    category = data[2]
                    diff_e = data[3]
                    diff_m = data[4]
                    bpm = data[5]
                    notes_e = data[6]
                    notes_m = data[7]
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
        logger(f"【{ctx.guild.name}】{ctx.author.name}: {CMDPREF}search {arg}")
        c = command_parser(arg)
        try:
            res = search_chunirec(level=c[0][0], level_range=c[0][1], category=c[1][0], artist=c[2][0], notes=c[3][0], notes_range=c[3][1], bpm=c[4][0], bpm_range=c[4][1], difficulty=c[5][0])
            if (lr := len(res)) > MAX_MUSICS:
                embed_mes = discord.Embed(title="Error", description=f"見つかった楽曲数({lr}曲)が{MAX_MUSICS}曲を超えるため、表示できません。", color=0xff0000)
            elif lr > 0:
                logger(f"以下の{lr}曲が見つかりました:")
                embed_mes = discord.Embed(title="検索結果", description=f"{lr}曲見つかりました。", color=0x00ff00)
                for m in res:
                    data = chunirec_parser(m)
                    title = data[0]
                    artist = data[1]
                    category = data[2]
                    diff_e = data[3]
                    diff_m = data[4]
                    bpm = data[5]
                    notes_e = data[6]
                    notes_m = data[7]
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
        await ctx.send(HELPMES)

class maimaiSelector(commands.Cog):
    pass

class OngekiSelector(commands.Cog):
    pass
