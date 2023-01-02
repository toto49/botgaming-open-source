import discord
import datetime



token = "votre token"
x = datetime.datetime.utcnow()
date_embed = f"Envoyé le {x.day}/{x.month}/{x.year} à {x.hour}:{x.minute}"


invite ="https://discord.com/api/oauth2/authorize?client_id=806045842631819265&permissions=8&scope=bot%20applications.commands"
support ="https://discord.gg/YXzJ7nXwDm"


fhelp = discord.Embed(title = "Voilà les commandes du bot.", description = f"Le préfixe du bot est `€`", color = 0x71368a)
fhelp.add_field(name= "__``Information``__", value= "userinfo, avatar, serverinfo, botinfo")
fhelp.add_field(name="__``modération``__", value="ban, unban, mute, unmute, kick, clear")
fhelp.add_field(name="__``administration``__", value="lock, unlock, clone, delete, say, addrole, rename")
fhelp.add_field(name="__``utilitaires``__", value="suggest")
fhelp.add_field(name= "__``Fun``__", value= "tirage, transchi")




funFact = ["L'eau mouille", 
			"Le feu brule", 
			"Lorsque vous volez, vous ne touchez pas le sol", 
			"Winter is coming", 
            "Mon créateur est invisible", 
			"Il n'est pas possible d'aller dans l'espace en restant sur terre", 
			"La terre est ronde",
			"La moitié de 2 est 1",
			"7 est un nombre heureux",
			"Les allemands viennent d'allemagne",
			"Le coronavirus est un virus se répandant en Europe, en avez vous entendu parler ?",
			"J'apparais 2 fois dans l'année, a la fin du matin et au début de la nuit, qui suis-je ?",
			"Le plus grand complot de l'humanité est",
			"Pourquoi lisez vous ca ?"]


guild_ids = [767453023198511244]

status = ["€help",
		"Le serveur support",
		"passionnément mes développeurs",
		"€invite",
		"version 3.0"]
