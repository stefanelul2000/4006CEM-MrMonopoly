# Discord Bot
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
    greetings=["I've been expecting you"]
    await member.create_dm()
    await member.dm_channel.send(f'{member.name}, welcome to my Discord Server, {greetings}')


@client.event
async def on_message(message):
    id = client.get_guild(484842929865883648)
    channels = ["bot"]
    greetings=['where have you been',"I've been expecting you",'how can I help you today']

    if str(message.channel) in channels:
        if message.content.find("Hello","hello") != -1:
            await message.channel.send(f"Hi there {message.author.name}, {random.choice(greetings)} !") 
        elif message.content == "!users":
            await message.channel.send(f"""This server has {id.member_count} member(s)!""")
        elif message.content == "!members":
            await message.channel.send(f"""This server has {id.member_count} member(s)!""")    

client.run(token)