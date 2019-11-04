# Discord Bot
# Creaded by Mono in 2019
#Import python libs
import os
import random
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from dotenv import load_dotenv
import asyncio
import datetime
import time

#Import python external files
import db
import gif
import graph
import analyse_text
import buy as purchase

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

client = discord.Client()
bot_prefix = "$"
client = commands.Bot(command_prefix=bot_prefix)


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
            await channel.send(gif.gif_response('welcome'))


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
            await message.channel.send(gif.gif_response('hello'))
        elif message.content == "!users":
            await message.channel.send(f"""This server has {id.member_count} member(s)!""")
        elif message.content == (f"{client.user} How many Members does the server have?"):
            await message.channel.send(f"""This server has {id.member_count} member(s)!""")
        elif message.content == "!thanks":
            await message.channel.send(f"{random.choice(thanks)} {message.author.name}")
            await message.channel.send(gif.gif_response('thanks'))         
    for word in bad_words:
        if message.content.count(word) > 0:
            await message.channel.purge(limit=1)
            await message.channel.send("Words like this are not permited in this server!")
    await client.process_commands(message)  

@client.command()
async def ask(ctx,*,arg):
    await ctx.send("Working on it...")
    channel = ctx.message.channel
    myOrganisation , myTimeFrame, myDays = analyse_text.process_text(arg)
    print(myOrganisation, myTimeFrame, myDays)
    graph.information_type("closed",time_scale=myTimeFrame,days=myDays,company_name=myOrganisation)
    await channel.purge(limit=1,check=None,bulk=True)
    await ctx.send(file=discord.File('stockImage.png'))
    await ctx.send(f"Here you go {ctx.author.mention}, showing you {myOrganisation} stock.")
    await asyncio.sleep(1)
    await ctx.send(gif.gif_response('looks expensive'))

@client.command()
async def join(ctx):
    ajoined = db.member_already_joined(ctx.author.id)
    post = {"_id":ctx.author.id,"name":ctx.author.name,"balance":5000}
    if ctx.author.id == ajoined:
        await ctx.send("You can't join the stock market more than one time!")
    else:  
        db.member_join(post)
        await ctx.send(f'{ctx.author.mention} you have now joined the stock market!')
        await ctx.send("Here are 5000 USD to start, enjoy!")
        await ctx.send(gif.gif_response("throwing money"))
    
@client.command()
async def buy(ctx,*,arg):
    if purchase.buy_stock(ctx.author.id,arg) == False:
        await ctx.send("Sorry, you can't buy this stock, you don't have enough money!")
    else:
        await ctx.send("Thanks for your purchase!")
        await ctx.send(gif.gif_response("empty wallet"))   

@client.command()
async def balance(ctx):
    wallet = db.get_user_balance(ctx.author.id)
    await ctx.send(f'You current balance is {wallet} USD')


#View portfolio
@client.command()
async def portfolio(ctx):
    portfolio_dic = db.get_portfolio(ctx.author.id)
    temp_counter = 0
    #embed = discord.Embed(title="Title", description="Desc", color=0x00ff00)
    #embed.add_field(name="Field1", value="hi", inline=False)
    #embed.add_field(name="Field2", value="hi2", inline=False)
    portfolio_embed = discord.Embed(title ="Portfolio", description = "Stocks you own", color = 0x00ff00)



    for stock_listing in portfolio_dic:
        for time_val in portfolio_dic[time_val]:
            

        paragraph =f"""

            Date:{time_val}

                Price:{share_price}

                Shares:{number_of_shares}
         """

    """
    for stock_listing in portfolio_dic:
        portfolio_embed.add_field(name = stock_listing,value="" )
        for time_val in portfolio_dic[stock_listing]:
            #share_list = "    " + str( portfolio_dic[stock_listing][time_val]) 
            portfolio_embed.add_field(name = portfolio_dic[stock_listing] ,value= portfolio_dic[stock_listing][time_val], inline = True  )

            print(time_val)
        #print(str(stock_listing[time_val]))     
         #  portfolio_embed.add_field(name = "" ,value=  str(stock_listing[time_val]))
    """
        
    await ctx.send(embed= portfolio_embed)
#    await ctx.send(str(portfolio))

@client.command(pass_context = True)
async def clear(ctx, ammount=100):
    channel = ctx.message.channel
    await channel.purge(limit=ammount,check=None,bulk=True)

client.run(token)