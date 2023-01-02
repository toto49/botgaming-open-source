from dis import disco
from unicodedata import name
import discord
from discord import channel
from discord import embeds
from discord.ext import commands, tasks
import random
from discord.ext.commands import Bot
from discord import Client, Intents, Embed
import asyncio
from discord.ext.commands import cooldown, BucketType
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord_slash.model import SlashCommandPermissionType
import os
import annexe 
import mutecode

custom_prefixes = {}
default_prefixes = ['€']
async def determine_prefix(bot, message):
    guild = message.guild
    if guild:
        return custom_prefixes.get(guild.id, default_prefixes)
    else:
        return default_prefixes

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix = determine_prefix, intents=intents)
bot.remove_command("help")
slash= SlashCommand(bot, sync_commands= True, sync_on_cog_reload= True)
@bot.command()
@commands.has_permissions(administrator = True)
@commands.guild_only()
async def setprefix(ctx, *, prefixes=""):
    custom_prefixes[ctx.guild.id] = prefixes.split() or default_prefixes
    embed = discord.Embed(title = "Setprefix", description = f"Le préfixe à été changé en `{prefixes}`", color = 0x90bc1)
    await ctx.send(embed = embed)
    await ctx.message.delete()

#@bot.event
#async def on_reaction_add(reaction, user):
    #await reaction.message.add_reaction(reaction.emoji)

"""
Pour chaque fichiers dans le dossiers ./cogs, le load_extension est automatique
"""
def loadCog():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f"cogs.{filename[:-3]}")

@bot.event
async def on_ready():
    channel = bot.get_channel(827049972993884160)
    embed = discord.Embed(title = "Bot en ligne", description = f"Ping: **{round(bot.latency*1000)}ms**", color = 0x1fff00)
    embed.set_footer(text = annexe.date_embed)
    await channel.send(embed = embed)
    print("Bot en ligne")
    changeStatus.start()
    loadCog()

#unload
@bot.command()
async def unload(ctx, name=None):
    if ctx.author.id == 703587895658676224 or ctx.author.id == 756967736348901518:
        if name:
            try:
                await ctx.message.delete()
                bot.unload_extension(name)
                await ctx.send(f"Le fichier **{name}.py** à bien été unload par {ctx.author.mention}.")
            except:
                await ctx.message.delete()
                await ctx.send("Impossible")

    else:
        return await ctx.send("Commande inconnue")

#reload
@bot.command()
async def reload(ctx, name=None):
    if ctx.author.id == 703587895658676224 or ctx.author.id==756967736348901518:
        if name:
            if name == "main":
                return await ctx.send("Vous ne pouvez pas recharger ce fichier.")
            try:
                bot.load_extension(name)
                await ctx.message.delete()
                await ctx.send(f"Le fichier **{name}.py** à bien été reload par {ctx.author.mention}.")
            except:
                bot.unload_extension(name)
                bot.load_extension(name)
                await ctx.message.delete()
                await ctx.send(f"Le fichier **{name}.py** à bien été reload par {ctx.author.mention}.")
                
        else:
            await ctx.message.delete()
            await ctx.send("Précisez un fichier à recharger.")
    else:
        return await ctx.send("Commande inconnue")



def isOwner(ctx):
	return ctx.message.author.id == 756967736348901518 or ctx.author.id==703587895658676224
	
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title = " <a:nop:794520827546697768> Erreur  <a:nop:794520827546697768> ", description = "Oups... cette commande n'existe pas. \nFaite €help pour connaitre la liste des commandes ", color = 0xfe3d39)
        await ctx.send(embed = embed)
        await ctx.message.delete()
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Il manque un argument ")
    #elif isinstance(error, commands.BotMissingPermissions): 
        #erreur = "" 
        #for err in error.missing_perms: 
            #erreur += f"``{err}``," 
        #erreur = erreur[:-1]
        #print("test")
        #print(erreur)
        return await ctx.send(f"{error}") 
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(name = "Erreur de permissions", description = "<a:nop:794520827546697768> Vous n'avez pas la permissions d'exécuter cette commande <a:nop:794520827546697768>", color=0xfe3d39)
        await ctx.send(embed =embed)
    elif isinstance(error, commands.CheckFailure): 
        await ctx.send("Oups cette commande ne peut être effectuée. Merci de contacter les développeurs sur le serveur support")
        channel = bot.get_channel(783388223728255006)
        await channel.send("une erreur c'est produit lors de l'éxécution d'une commande")
    
    
@bot.event
async def on_guild_join(guild):
    logs = bot.get_channel(814483785281175573)
    user = (len(bot.users))
    server = (len(bot.guilds))
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send('Hey **{}** mon prefix est ``€``'.format(guild.name))
            embed = discord.Embed(name= "Bot ajouté", description= f"Le serveur **{guild.name}** m'a ajouté  \n\nje suis désormais sur **{server}** serveurs et je totalise **{user}** utilisateurs ", color = 0x1fff00)
            await logs.send(embed = embed)
        break

@bot.event
async def on_guild_remove(guild):
    logs = bot.get_channel(814483785281175573)
    user = (len(bot.users))
    server = (len(bot.guilds))
    embed = discord.Embed(name= "Bot retiré", description= f"Le serveur **{guild.name}** m'a retiré  \n\nje suis désormais sur **{server}** serveurs et je totalise **{user}** utilisateurs ", color =  0xfe3d39)
    await logs.send(embed = embed)  
      
  
def isPair(ctx):
	return ctx.message.author.id % 2 == 0

@bot.command()
@commands.check(isPair)
@commands.has_permissions(manage_messages = True)
async def pair(ctx):
	await ctx.send("Vous remplissez toutes les conditions !")
	
@bot.command()
@commands.has_permissions(manage_roles= True)
async def addrole(ctx, member : discord.Member, *,nom):
    roleMembre = ""
    roles = ctx.guild.roles
    for role in roles:
        if role.name == nom:
            roleMembre = role
    if roleMembre == "":
        roleMembre = await ctx.guild.create_role(name = nom, reason = "Un membre a fait la commande role.")
    await member.add_roles(roleMembre, reason = "commande")
    await ctx.reply("Role ajouté")
    
@tasks.loop(seconds = 10)
async def compter():
	global count
	channel = bot.get_channel(806048616254799913)
	await channel.send(count)
	print("count")
	count += 1
   
@bot.command()
async def coucou(ctx):
    await ctx.send("**Salut ! Je suis un bot discord super sympa qui peut vous réserver pleins de surprises!**")
    await ctx.message.delete()
    
@bot.command()
async def maj(ctx):
    embed = discord.Embed(title = "Informations mise à jour", description = "Possibilité de bugs ou d'absence de réponse de commandes. Informez nous des problèmes sur notre serveur support en faisant €invite")
    await ctx.send(embed = embed)
    await ctx.message.delete()


def checkAuthor(ctx):
    owners = [703587895658676224, 756967736348901518]
    return ctx.message.author.id in owners




@bot.command()
async def tirage(ctx):
	await ctx.send("La roulette commencera dans 30 secondes. Envoyez \"jouer\" dans ce channel pour y participer et peut être remporter le tirage au sort.")
	
	players = []
	def check(message):
		return message.channel == ctx.message.channel and message.author not in players and message.content == "jouer"

	try:
		while True:
			participation = await bot.wait_for('message', timeout = 30, check = check)
			players.append(participation.author)
			#print("Nouveau participant : ")
			#print(participation)
			await ctx.send(f"**{participation.author.name}** participe au tirage ! Le tirage commence dans 30 secondes")
	except: #timeout
		await ctx.send("Demarrage du tirage préparez vous a perdre")

	gagner = ["ban", "kick", "role personnel", "mute", "gage", " droit de se faire spam", "rien du tout"]

	await ctx.send("Le tirage va commencer  dans 3...")
	await asyncio.sleep(1)
	await ctx.send("2")
	await asyncio.sleep(1)
	await ctx.send("1")
	await asyncio.sleep(1)
	loser = random.choice(players)
	price = random.choice(gagner)
	await ctx.send(f"Le gagnant qui a gagné un **{price}** est...")
	await asyncio.sleep(1)
	await ctx.send("**" + loser.name + "**" + " !")
	await ctx.message.delete()



@bot.command()
async def invite(ctx):
    embed = discord.Embed(title = "Liens utiles", description = f"Voilà quelques liens utiles : \n\n[Inviter le bot]({annexe.invite}) \n[Trello du bot](https://trello.com/b/UC6L9jFI/botgaming)\n[Serveur support du bot]({annexe.support})\n[twitter officiel](https://twitter.com/i/lists/1332383633668190213)", color = 0x71368a)
    await ctx.send(embed = embed)
    await ctx.message.delete()




@bot.command()
@commands.check(isOwner)
async def start(ctx, secondes = 5):
	changeStatus.change_interval(seconds = secondes)
	changeStatus.is_running()

@tasks.loop(seconds = 5)
async def changeStatus():
	game = random.choice(annexe.status)
#	await bot.change_presence(activity=discord.Streaming(name= game))

	
	await bot.change_presence(activity=discord.Streaming(name = game, url = "https://www.twitch.tv/atom_497"))


        
@bot.command()
async def botgaming(ctx):
    embed = discord.Embed(title = "botgaming ", description = "Hey ! Voulez vous que j'égaye la vie de votre serveur ? : Clique sur l'image")
    embed.add_field(name = "invite", value = f"[clique içi]({annexe.invite})", inline = False)
    await ctx.send(embed = embed)
    await ctx.send("https://s1.lprs1.fr/images/2019/11/19/8197029_118%20-%20piratage.jpg")


@slash.slash(name="ping", guild_ids=[767453023198511244], description="donne le ping du bot")
async def ping(ctx):	
    await ctx.send(f"Pong!  {round(bot.latency*1000)}ms)")


bot.run(annexe.token)
