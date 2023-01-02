import discord
from discord.ext import commands, tasks
import asyncio
import random
import json
import datetime
import annexe
import mutecode

def setup(bot):
    bot.add_cog(commandesModo(bot))

class commandesModo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def martin1(self, ctx):
        await ctx.send("Yes, ça a marché ! <a:blob:786894343499808799>")
    
    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, user : discord.User, *, reason = "Aucune raison n'a été donné"):
        embed = discord.Embed(title = "Kick", description = f"{user.name} a été expulsé de ce serveur.", color = 0x90bc1)
        embed.add_field(name = "Modérateur :", value = ctx.author.name, inline = True)
        embed.add_field(name = "Raison", value = f"{reason}", inline = False )
        await ctx.guild.kick(user, reason = reason)
        await ctx.send(embed = embed)
        #await ctx.message.delete() 
        
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Oups... Vous avez oublié d'indiquez qui je dois expulser.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("Vous n'avez pas la permission d'expulser des membres")
        if isinstance(error.original, discord.Forbidden):
            await ctx.send("Je n'ai pas la permission d'expulser quelqu'un.")



    @commands.command() 
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, user : discord.User, *, reason = "Aucune raison n'a été donné"):
        await ctx.guild.ban(user, reason = reason)
        reason = "".join(reason)
        embed = discord.Embed(title = "**Banissement**", description = "Le marteau du ban a encore frapper !", color=0xfe3d39)
        embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        embed.set_thumbnail(url = "https://discordemoji.com/assets/emoji/BanneHammer.png")
        embed.add_field(name = "Membre banni :", value = user.name, inline = True)
        embed.add_field(name = "Raison", value = reason, inline = True)
        embed.add_field(name = "Modérateur :", value = ctx.author.name, inline = True)
        embed.set_footer(text = random.choice(annexe.funFact))
        
        await ctx.send(embed = embed)
        await ctx.message.delete()

    

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Vous devez indiquez le membre à bannir.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("Mmmh... vous n'avez pas les permissions pour bannir.")
        if isinstance(error.original, commands.BotMissingPermissions):
            await ctx.send("Oups... Il semblerait que je n'ai pas les permissions pour bannir des membres.")

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, user, *reason):
        reason = " ".join(reason)
        userName, userId = user.split("#")
        bannedUser = await ctx.guild.bans()
        for i in bannedUser:
            if i.user.name == userName and i.user.discriminator == userId:
                await ctx.guild.unban(i.user, reason = reason)
                await ctx.send(f"**unban** \n{user} a été unban pour la raison suivante :{reason}")
                return
        await ctx.send(f"L'utlisateur {user} n'a pas été banni sur se serveur.")
        #await ctx.message.delete()
        
    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Vous devez indiquez le membre à débannir au format `user#0001`")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("Vous n'avez pas la permissions de débannir quelqu'un.")
        if isinstance(error.original, discord.Forbidden):
            await ctx.send("Je n'ai pas la permission de débannir des personnes.")
            

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def mute(self, ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseignée"):
        mutedRole = await mutecode.getMutedRole(ctx)
        embed = discord.Embed(title = "Mute", description = f"{member.mention} a bien été mute", color = 0xfe3d39)
        embed.add_field(name = "Raison", value = f"{reason}")
        await member.add_roles(mutedRole, reason = reason)
        await ctx.send(embed = embed)
        await ctx.message.delete()
        
        
    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Vous devez indiquer la personne que vous voulez interdire de parler.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("J'ai l'impression que vous n'avez pas les permissions requises pour interdire quelqu'un de parler.")
        if isinstance(error.original, discord.Forbidden):
            await ctx.send("Mmmh... Je n'ai pas les permissions requises pour interdire à quelqu'un de parler.")

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def unmute(self, ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
        mutedRole = await mutecode.getMutedRole(ctx)
        await member.remove_roles(mutedRole, reason = reason)
        embed = discord.Embed(title = "Unmute", description = f"{member.mention} a été unmute !", color = 0x1fff00)
        embed.add_field(name = "Raison", value = f"{reason}")
        await ctx.send(embed = embed)
        await ctx.message.delete()
        
    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Vous devez indiquer la personne à réautoriser à parler.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("J'ai l'impression que vous n'avez pas les permissions requises pour réautoriser des personnes à parler")
        if isinstance(error.original, discord.Forbidden):
            await ctx.send("Mmmh... Je n'ai pas les permissions requises pour réautoriser quelqu'un à parler")
