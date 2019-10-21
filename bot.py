# Discord Bot
import os
import random
import discord
from gengraph import *

from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    activity = discord.Game(name="Python")
    await client.change_presence(status=discord.Status.online, activity=activity)

@client.event
async def on_member_join(member):
    greetings=["I've been expecting you"]
    role= discord.utils.get(member.guild.roles, name="Users")
    dm = await member.create_dm()

    await member.add_roles(role)

    await dm.send(f'{member.name}, welcome to my Discord Server, {random.choice(greetings)}')

    for channel in member.guild.channels:
        if str(channel.name) == "welcome":
            await channel.send(f"""Welcome to the server {member.mention}""")


@client.event
async def on_message(message):
    id = client.get_guild(484842929865883648)
    channel = client.get_channel(628551773455646721)
    channels = ["bot"]
    greetings=['where have you been',"I've been expecting you",'how can I help you today']
    bad_words = ["fuck", "Fuck", "dick","Dick"]
    olddays = str
    stockname = str

    if str(message.channel) in channels:
        if message.content.find("!hello") != -1:
            await message.channel.send(f"Hi there {message.author.name}, {random.choice(greetings)} !") 
        elif message.content == "!users":
            await message.channel.send(f"""This server has {id.member_count} member(s)!""")
        elif message.content == (f"{client.user} How many Members does the server have?"):
            await message.channel.send(f"""This server has {id.member_count} member(s)!""")
        elif message.content == (f"!stock {olddays} {stockname}"):
            information_type("close",{olddays},{stockname})
            await channel.send(file=discord.File('stockImage.png'))
            

    for word in bad_words:
        if message.content.count(word) > 0:
            print("A bad word was said")
            await message.channel.purge(limit=1)
            await message.channel.send("Words like this are not permited in this server!")

    

client.run(token)