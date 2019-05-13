from scraper import getlink, pokescraper, getLegos
import json
import discord
from discord.ext import commands

with open("auth.json", "r") as read_file:
	data = json.load(read_file)
TOKEN = data.get("token")
prefix = data.get("prefix")

bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_ready():
    await bot.change_presence(activity = discord.Game(name="=dex"))
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith(prefix):
        msg = message.content[len(prefix):].split(' ')
        cmd = msg[0]
        
        if(cmd == "help"):
            embed = discord.Embed(color=0xFF0000)
            msg = "`=dexid [pokemon]` identifies a pokemon\n=`dexscan [pokemon]` indepth identification of a pokemon\n`=dexbrick` lookup lego set"
            embed.add_field(name="Commands", value=msg, inline=True)
            embed.set_footer(text="Made by Nikomix")
            await message.channel.send(embed=embed)

        if(cmd == "id"):
            query = "".join(msg[1:])
            t = getlink(query, ["pokedex", "site:serebii.net"], ["pokedex", "serebii"], ["google", "3dpro", "search"])
            if(t): 
                data = pokescraper(t)
                if(data):
                    data = json.loads(data)
                    embed = discord.Embed(color=0xFF0000)
                    embed.set_image(url=data["thumb"])
                    await message.channel.send(data["id"] + " - " + data["name"])
                    embed.set_footer(text="Made by Nikomix")

                    await message.channel.send(embed=embed)
                else:
                    await message.channel.send("Data for this pokemon cannot be retrieved")
            else:
                await message.channel.send("No results found")

        if(cmd == "scan"):
            query = "".join(msg[1:])
            t = getlink(query, ["pokedex", "site:serebii.net"], ["pokedex", "serebii"], ["google", "3dpro", "search"])
            if(t): 
                data = pokescraper(t)
                if(data):
                    data = json.loads(data)
                    embed = discord.Embed(color=0xFF0000)
                    embed.set_image(url=data["thumb"])
                    await message.channel.send(data["id"] + " - " + data["name"])
                    msg = ""
                    for x in data["abilities"]: msg += x + "\n"
                    embed.add_field(name="Abilities", value=msg.replace("-", " "), inline=False)
                    if(data["hidden"]):
                        msg = ""
                        for x in data["hidden"]: msg += x + "\n"
                        embed.add_field(name="Hidden Abilities", value=msg.replace("-", " "), inline=False)
                    msg = "HP: {}\nATK: {}\nDEF: {}\nSPATK: {}\nSPDEF: {}\nSPD: {}".format(data["stats"]["hp"], data["stats"]["atk"], data["stats"]["def"], data["stats"]["spatk"], data["stats"]["spdef"], data["stats"]["spd"])
                    embed.add_field(name="Stats", value=msg, inline=True)
                    embed.set_footer(text="Made by Nikomix")

                    await message.channel.send(embed=embed)
                else:
                    await message.channel.send("Data for this pokemon cannot be retrieved")
            else:
                await message.channel.send("No results found")

        if(cmd == "brick"):
            query = "".join(msg[1:])
            t = getlink(query, ["set", "site:brickset.com"], ["sets"], ["google", "theme", "query"])
            if(t): 
                data = getLegos(t)
                if(data):
                    data = json.loads(data)
                    embed=discord.Embed(title=data["name"] + " (" + data["year"] + ") - " + data["id"], url=data["brickUrl"], color=0xFF0000)
                    #await message.channel.send(data["name"] + " (" + data["year"] + ") - " + data["id"])
                    embed.set_image(url=data["thumb"])
                    embed.add_field(name="Pieces", value=data["pieces"], inline=False)
                    embed.add_field(name="Price", value=data["priceUS"] + " USD", inline=False)
                    embed.set_footer(text="Made by Nikomix")                    
                    await message.channel.send(embed=embed)
                else:
                    await message.channel.send("Data for this set cannot be retrieved")
            else:
                await message.channel.send("No results found")

if __name__ == '__main__':
    bot.run(TOKEN)