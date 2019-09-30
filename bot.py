# bot.py
import os
import random
import discord

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
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord Server!'
    )


@client.event
async def on_message(message):
    id = client.get_guild(484842929865883648)
    channels = ["bot"]

    if str(message.channel) in channels:
        if message.content.find("Hello") != -1:
            await message.channel.send(f"HI there {message.author.name}!") 
        elif message.content == "!users":
            await message.channel.send(f"""This server has {id.member_count} member(s)!""")

client.run(token)