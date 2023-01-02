import discord
from discord.ext import commands, tasks
import asyncio
import random
import json
import datetime
from setuptools import Command
import annexe
import mutecode




def setup(bot):
    bot.add_cog(commandesUtile(bot))

class commandesUtile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases =["su"])
    async def suggest(self, ctx):
        question = await ctx.send("Envoyez votre suggestion")
        await ctx.message.delete()
        
        def checkMessage(message):
            return message.author == ctx.message.author and ctx.message.channel == message.channel
        
        suggestion = await self.bot.wait_for("message", timeout = 3600, check = checkMessage)
        embed = discord.Embed(title = "Une suggestion a été proposée !", description = f"**{suggestion.content}**", color = 0x71368a)
        embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        embed.set_footer(text = annexe.date_embed)
        message = await ctx.send(embed = embed)
        await suggestion.delete()
        await question.delete()
        await message.add_reaction("<a:valid:794520750802731020>")
        await message.add_reaction("<:inactif:791679353956073503>")
        await message.add_reaction("<a:nop:794520827546697768>")


    @commands.command()
    async def help(self, ctx):
        message= await ctx.send(embed = discord.Embed(title = "Comment voulez vous recevoir la liste les commandes ? \ncocher 📩 pour les recevoirs  en mp \ncocher 🧾 pour les recevoirs dans se salon \ncocher ❌ pour annuler ", color = 0x71368a))
        await message.add_reaction("📩")
        await message.add_reaction("🧾")
        await message.add_reaction("❌")
        
        def checkEmoji(reaction, user):
            return ctx.message.author == user and message.id == reaction.message.id and(str(reaction.emoji) == "📩" or str(reaction.emoji) == "❌" or str(reaction.emoji) == "🧾")
        
        reaction, user = await self.bot.wait_for("reaction_add", timeout = 60, check = checkEmoji)
        if reaction.emoji == "📩":
            await message.edit(embed = discord.Embed(title = f"Les commandes vous ont été envoyées en message privé", color = 0x71368a))
            await ctx.author.send(embed = annexe.fhelp)
            await message.remove_reaction(reaction, user)
        if reaction.emoji == "🧾":
            await message.edit(embed = annexe.fhelp)
            await message.remove_reaction(reaction, user)
        if reaction.emoji == "❌":
            await message.edit(embed = discord.Embed(title = f"Commande annuler", color = 0xfe3d39))
            await message.remove_reaction(reaction, user)
            await asyncio.sleep(10)
            await message.delete()
        await ctx.message.delete()
