@bot.command()
async def button(ctx):
    await ctx.send(
        "Boutons WTF !",
        components = [
            Button(label = "Style 1", style = 1), 
            Button(label = "Style 2", style = 2),
            Button(label = "Style 3", style = 3),
            Button(label = "Style 4", style = 4),
            Button(label = "Style 5", style = 5, url = "https://niewia.fr")
        ]
    )
    #check = lambda i: i.component.label.startswith("WOW")
    interaction = await bot.wait_for("button_click")
    await interaction.respond(content = "Bouton cliqué !")

@bot.command()
async def reply(ctx):
    await ctx.reply('Réponse')

@bot.command()
async def replynomention(ctx):
    await ctx.reply('Réponse', mention_author = False)
