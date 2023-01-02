import discord
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord_slash.model import SlashCommandPermissionType
import annexe
import slash
@slash.slash(name="help",guild_ids= annexe.guild_ids, description="donne le ping du bot", options=[
	create_option(
		name="choisir ", 
		description="indiquez ou vous voulez afficher le help", 
		option_type=3,
		required=True,
		choices=[
			create_choice(
				name="mp",
				value="y"
			),
			create_choice(
				name="dans ce channel",
				value="n"
			)
		]
	),
	
])
async def help(ctx, choisir):


    if choisir == "y":
        embed = discord.Embed(title = f"Les commandes vous ont été envoyées en message privé", color = 0x71368a, hidden = True)
        await ctx.author.send(embed = annexe.fhelp)
        await ctx.send(embed = embed, hidden = True)
    elif choisir == "n":
        await ctx.send(embed = annexe.fhelp)
         