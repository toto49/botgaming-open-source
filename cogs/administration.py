from email import message
import discord
from discord.ext import commands, tasks
import asyncio
import random
import json
import datetime

def setup(bot):
    bot.add_cog(commandesAdmin(bot))

class commandesAdmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
   
        
    @commands.command()
    async def martin2(self, ctx):
        await ctx.send("Yes, ça a remarché ! <a:blob:786894343499808799>")
        
   
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel : discord.TextChannel=None, member : discord.Member = "Rien"):
        server = ctx.guild
        if member == "Rien":
            member = ctx.author
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(server.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(server.default_role, overwrite=overwrite)
        #await ctx.send("<a:valid:794520750802731020> error message <a:valid:794520750802731020> pb signaler au devellopeurs")
        message = await ctx.send(ctx.channel.mention + f" ***a été lock*** 🔒 ")
        await message.add_reaction("<a:nop:794520827546697768>")
        #embed = discord.Embed(title = f"serveur {server.name}", description = "", color = 0xfe3d39)
        #embed.add_field(name =ctx.channel.mention + f" *** a été lock*** 🔒 ", value = "test")
        #await ctx.send(embed=embed)
        await ctx.message.delete()
    
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, member : discord.Member = "Rien"):
        server = ctx.guild
        if member == "Rien":
            member = ctx.author
        await ctx.channel.set_permissions(server.default_role, send_messages=True)
        #await ctx.send("<a:valid:794520750802731020> error message <a:valid:794520750802731020> pb signaler au devellopeurs")
        message = await ctx.send(ctx.channel.mention + f" ***a été unlock*** 🔓 ")
        await message.add_reaction("<a:valid:794520750802731020>")
        #embed = discord.Embed(title = f"serveur {server.name}", description = "", color = 0xfe3d39)
        #embed.add_field(name = ctx.channel.mention + f" ***a été  unlock*** 🔓", value = f"par {member.mention}")
        #await ctx.send(embed = embed)
        await ctx.message.delete()

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def delete(self, ctx):
        await ctx.channel.delete()
        embed = discord.Embed(title=f" Channel #{ctx.channel.name} a été suprimé ",description=f"le salon a été suprimé par: {ctx.author.name}#{ctx.author.discriminator}", color = 0x90bc10)
        embed.set_footer(text=ctx.guild.name)
        await ctx.author.send(embed=embed)
    
    
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def nuke(self, ctx, member : discord.Member = "Rien"):
        server = ctx.guild
        if member == "Rien":
            member = ctx.author
        pos = ctx.channel.position
        channel = await ctx.channel.clone()
        await ctx.channel.delete()
        await channel.edit(position=pos)
        embed = discord.Embed(title = f" Channel #{ctx.channel.name} a été nuke ",description=f"Salon nuke par : {member.mention}", color = 0x90bc10)
        embed.set_footer(text = server.name)
        await channel.send(embed = embed)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def clone(self, ctx):
        pos = ctx.channel.position
        channel = await ctx.channel.clone()
        await channel.edit(position=pos)
        await ctx.send(ctx.channel.mention + "a été cloné")
        embed = discord.Embed(title=f"Channel #{ctx.channel.name} a été cloné",description=f"Cloné par: {ctx.author.name}#{ctx.author.discriminator}", color = 0x90bc10)
        #embed.add_field(name = "test", value = ctx.author.name.mention, inline = True)
        await channel.send(embed=embed)
        await ctx.message.delete()
        
        
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def clear(self, ctx, nombre : int):
        messages = await ctx.channel.history(limit = nombre + 1).flatten()
        for message in messages:
            await message.delete()
        reponse = await ctx.send(f"{nombre} messages suprimés")
        await asyncio.sleep(10)   
        await reponse.delete()
            
            
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Vous devez indiquer le nombre de message à supprimer.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("J'ai l'impression que vous n'avez pas les permissions requises pour supprimer des messages.")
        if isinstance(error.original, discord.Forbidden):
            await ctx.send("Mmmh... Je n'ai pas les permissions requises pour supprimer les messages.")



    @commands.command()
    @commands.has_permissions(administrator = True)
    async def say(self, ctx, *texte):
        await ctx.send(" ".join(texte))
        await ctx.message.delete()


    @commands.command()
    @commands.has_permissions(manage_nicknames = True)
    async  def rename(self, ctx, member: discord.Member, *, nick ="pseudo"):
        await member.edit(nick=nick)
        await ctx.send(f"le pseudo de {member.mention} a été changé")
        await ctx.message.delete() 



