

from unicodedata import name
import discord
from discord.ext import commands, tasks
from discord.ext.commands import cooldown, BucketType
import asyncio
import random
import json
import datetime
import annexe
from discord_slash import cog_ext
from discord.ext import commands
from discord_slash.cog_ext import cog_slash
from discord_slash.utils.manage_commands import create_option, create_choice


def setup(bot):
    bot.add_cog(commandesInfos(bot))

class commandesInfos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ["infoserver", "si"])
    async def serverinfo(self, ctx):
        server = ctx.guild
        serverCreate = server.created_at
        numberOfTextChannels = len(server.text_channels)
        numberOfVoiceChannels = len(server.voice_channels)
        serverDescription = server.description
        if serverDescription == None:
            serverDescription = "Ce serveur n'a pas de description"
        numberOfPerson = server.member_count
        serverName = server.name
        name = str(ctx.guild.name)
        description = str(ctx.guild.description)
        role_count = len(ctx.guild.roles)
        list_of_bots = [bot.mention for bot in ctx.guild.members if bot.bot]
        owner = str(ctx.guild.owner)
        id = str(ctx.guild.id)
        region = str(ctx.guild.region)
        memberCount = str(ctx.guild.member_count)
        icon = str(ctx.guild.icon_url)
        embed = discord.Embed(title=name, description = "``Informations du serveur``", color = 0x71368a)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_thumbnail(url=icon)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.add_field(name = f"Nom du serveur", value = serverName)
        embed.add_field(name = f"Description du serveur", value = serverDescription)
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="ID du serveur", value=id, inline=True)
        embed.add_field(name="Region", value=region, inline=True)
        embed.add_field(name='Nombre  de roles', value=str(role_count), inline=False)
        embed.add_field(name='roles le plus haut', value=ctx.guild.roles[-2], inline=False)
        embed.add_field(name='Bots:', value=(', '.join(list_of_bots)))
        embed.add_field(name = f"Nombre de personnes sur le serveur", value = numberOfPerson)
        embed.add_field(name = f"Nombre de salons", value = f"{numberOfTextChannels} salons textuels et {numberOfVoiceChannels} salons vocaux")
        embed.add_field(name = f"Date de création du serveur", value = serverCreate.strftime("Le %d/%m/%Y"))
        await ctx.send(embed = embed)
        await ctx.message.delete()
        
    @commands.command(aliases = ["infouser", "ui"])
    async def userinfo(self, ctx, member : discord.Member = "Rien"):
        server = ctx.guild
        if member == "Rien":
            member = ctx.author
        else:
            pass
        creation_date = member.created_at
        serverJoin = member.joined_at
        role_member = []
        for role in member.roles:
            if role.name != "@everyone":
                role_member.append(role.mention)
        roleDuMembre = role_member.reverse()
        roleDuMembre = " ".join(role_member)
        embed = discord.Embed(title = f"Informations de l'utilisateur `{member.name}`", description = None, color = 0x71368a)
        embed.set_author(name =  f"{member.name}", icon_url = member.avatar_url)
        embed.add_field(name = f"Mention de l'utilisateur", value = f"{member.mention}")
        embed.add_field(name = f"Tag de l'utilisateur", value = f"{member}")
        embed.add_field(name = f"Date de création du compte", value = creation_date.strftime("Le %d/%m/%Y à %H:%M"))
        embed.add_field(name = f"Rôles de l'utilisateur sur ce serveur", value = roleDuMembre, inline = False)
        embed.add_field(name = f"Serveur rejoint", value = serverJoin.strftime("Le %d/%m/%Y"))
        embed.add_field(name = f"ID", value = member.id)
        embed.set_footer(text = f"Demandé par {ctx.author} | Sur le serveur {server.name}")
        await ctx.send(embed = embed)
        await ctx.message.delete()      

    @commands.command()
    async def botinfo(self, ctx):
        server = ctx.guild
        serverName = server.name
        numberOfPerson = server.member_count
        user = (len(self.bot.users))
        servernb = (len(self.bot.guilds))
        embed = discord.Embed(title = "\nVoici les informations sur Botgaming", color= 0x71368a)
        embed.add_field(name = "__Mes créateurs :__", value = "*Nitrzm#1232* \n*atom497#6194*", inline = False)
        embed.add_field(name = "Nombre de personnes qui m'utilisent", value= f"Je suis sur **{servernb}** serveur et j'ai **{user}** utilisateurs")
        embed.add_field(name = "__Liens utiles__", value = f"[Inviter le bot]({annexe.invite}) \n[Trello du bot](https://trello.com/invite/b/UC6L9jFI/51f8daf859048c54905223158ba20a7a/botgaming)\n[Serveur support du bot]({annexe.support}) \n[Twitter officiel](https://twitter.com/Botgamingv2)", inline = False)
        embed.add_field(name = "Informations code", value = "Bot codé en python avec la librairie `discord.py`", inline = False)
        embed.add_field(name = "__Bot en ligne__", value = "<:online:777225969076797450>", inline = False)
        embed.set_footer(text = f"Commande effectuée sur {serverName}")
        await ctx.send(embed = embed)
        await ctx.message.delete()
        
    @commands.command(aliases = ["pp"] )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def avatar(self, ctx, member : discord.Member = "Rien"):
        if member == "Rien":
            member = ctx.author
        server = ctx.guild
        Avatar = member.avatar_url_as(size=1024)
        AvatarEmbed = discord.Embed(title = f"voici la pp de **{member}**", color = 0x71368a)
        AvatarEmbed.set_image(url = Avatar)
        await ctx.send(embed = AvatarEmbed)
        await ctx.message.delete()
        
    @avatar.error 
    async def avatar_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            message = await ctx.send(f"il reste {error.retry_after:.2f}s avant la fin du cooldown ")
            await asyncio.sleep(10)
            await ctx.message.delete()
            await message.delete()

    @commands.command(aliases = ["bienvenue"])
    async def bvn(self, ctx, user : discord.User):
        server = ctx.guild
        serverName = server.name
        memberCount = str(ctx.guild.member_count)
        embed = discord.Embed(title = f"Bienvenue sur le serveur **{serverName}**", color = 0x71368a )
        embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        embed.set_footer(text = random.choice(annexe.funFact))
        embed.add_field(name = "Une personne vous souhaite la bienvenue : " , value = ctx.author.name , inline = True)
        embed.add_field(name = "Nous sommes désormais:", value = f"{memberCount}")
        await ctx.send(user.mention)
        await ctx.send(embed = embed)
        await ctx.message.delete()


    @cog_ext.cog_slash(name="test", guild_ids=[767453023198511244], description="....",)
    async def test(self, ctx):	
        await ctx.send("coucou ")