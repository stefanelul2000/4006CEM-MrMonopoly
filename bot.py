# Discord Bot
import os
import random
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import graph
import analyse_text
import giphy_client
from giphy_client.rest import ApiException
#from pprint import pprint
from dotenv import load_dotenv
import time

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
giphy_token= os.getenv('GIPHY_TOKEN')

client = discord.Client()
bot_prefix = "$"
client = commands.Bot(command_prefix=bot_prefix)
api_instance = giphy_client.DefaultApi() #Giphy API

def search_gifs(query):
    try:
        return api_instance.gifs_search_get(giphy_token, query, limit=5, rating = 'g')

    except ApiException as e:
        return "Exception when calling DefaultApi->gifs_search_get: %s\n" % e

def gif_response(emotion):
    gifs = search_gifs(emotion)
    lst = list(gifs.data)
    gif = random.choices(lst)

    return gif[0].url

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    print(f'ID: {client.user.id}')
    activity = discord.Game(name="with stocks")
    await client.change_presence(status=discord.Status.online, activity=activity)

@client.event
async def on_member_join(member):
    greetings=["I've been expecting you"]
    role= discord.utils.get(member.guild.roles, name="Users")
    channels = ["bot"]
    dm = await member.create_dm()

    await member.add_roles(role)

    await dm.send(f'{member.name}, welcome to my Discord Server, {random.choice(greetings)}')

    for channel in member.guild.channels:
        if str(channel.name) == "welcome":
            await channel.send(f"""Welcome to the server {member.mention}""")
            await channel.send(gif_response('welcome'))


@client.event
async def on_message(message):
    id = client.get_guild(484842929865883648)
    channel = client.get_channel(635976394836279297)
    channels = ["bot"]
    greetings=['where have you been',"I've been expecting you",'how can I help you today']
    thanks=["Happy to help","No worries"]
    bad_words = ["fuck", "Fuck", "dick","Dick"]
    

    if str(message.channel) in channels:
        if message.content.find("!hello") != -1:
            await message.channel.send(f"Hi there {message.author.name}, {random.choice(greetings)} !") 
            await message.channel.send(gif_response('hello'))
        elif message.content == "!users":
            await message.channel.send(f"""This server has {id.member_count} member(s)!""")
        elif message.content == (f"{client.user} How many Members does the server have?"):
            await message.channel.send(f"""This server has {id.member_count} member(s)!""")
        elif message.content == "!thanks":
            await message.channel.send(f"{random.choice(thanks)} {message.author.name}")
            await message.channel.send(gif_response('thanks'))         
    for word in bad_words:
        if message.content.count(word) > 0:
            await message.channel.purge(limit=1)
            await message.channel.send("Words like this are not permited in this server!")
    await client.process_commands(message)

@client.command()
async def ask(ctx,*,arg):
    myOrganisation , myTimeFrame, myDays = analyse_text.process_text(arg)
    graph.information_type("closed",time_scale=myTimeFrame,days=myDays,company_name=myOrganisation)
    await ctx.send("Working on it...")

    await ctx.send(file=discord.File('stockImage.png'))
    await ctx.send(f"Here you go {message.author.name}, showing you {myOrganisation} stock.")

@client.command(pass_context = True)
async def clear(ctx, ammount=100):
    channel = ctx.message.channel
    await channel.purge(limit=ammount,check=None,bulk=True)

client.run(token)