import discord
from discord.ext import commands, tasks
import asyncio
import random
import json
import datetime

def setup(bot):
    bot.add_cog(commandesFun(bot))

class commandesFun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def martin4(self, ctx):
        await ctx.send("Yes, ça a marché ! <a:blob:786894343499808799> ")

    @commands.command()
    async def transchi(self, ctx, *text):
        chineseChar = "丹书匚刀巳下呂廾工丿片乚爪冂口尸Q尺丂丁凵V山乂Y乙"
        chineseText = []
        for world in text:
            for char in world:
                if char.isalpha():
                    index = ord(char) - ord("a")
                    transformmed = chineseChar[index]
                    chineseText.append(transformmed)
                else:
                    chineseText.append(char)
            chineseText.append(" ")
        await ctx.send(" ".join(chineseText))
        await ctx.message.delete()

