# import discord
# from discord.ext import commands

# from .log import logger
# from .random_select import random_select, random_select_international


def command_parser(command):
    cl = command.split()
    for e in range(len(cl)):
        if cl[e].lower() == "none":
            cl[e] = "-"
        elif ":" in cl[e]:
            e_temp = cl[e].split(":")
            cl[e] = [e_temp[0], e_temp[1]]
    return cl


class ChunithmSelector(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def random(self, ctx):
        pass


class maimaiSelector(commands.Cog):
    pass


class OngekiSelector(commands.Cog):
    pass
