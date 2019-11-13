# Discord Bot
# Creaded by Mono in 2019
#Import python libs
import os
import random
import discord
from discord.ext import commands
import asyncio

#Import python external files
import db
import gif
import graph
import analyse_text
import buy as purchase
import sell as selling
#from custom_ML.query_model import categorise_sentence as model_query
import leaderboard


token = os.environ.get('DISCORD_TOKEN')
client = discord.Client()
bot_prefix = "$"
client = commands.Bot(command_prefix=bot_prefix)

@client.event #Prints when bot has successfullly connected to Discord
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    print(f'ID: {client.user.id}')
    activity = discord.Game(name="with stocks")
    await client.change_presence(status=discord.Status.online, activity=activity)

@client.event #Welcomes user when joining the server
async def on_member_join(member):
    greetings=["I've been expecting you"]
    role= discord.utils.get(member.guild.roles, name="Users")
    dm = await member.create_dm()

    await member.add_roles(role)

    await dm.send(f'{member.name}, welcome to my Discord Server, {random.choice(greetings)}')

    for channel in member.guild.channels:
        if str(channel.name) == "welcome":
            await channel.send(f"""Welcome to the server {member.mention}""")
            await channel.send(gif.gif_response('welcome'))

@client.event
async def on_message(message):
    guild_id = client.get_guild(484842929865883648)
    channels = ["bot"]
    greetings=['where have you been',"I've been expecting you",'how can I help you today']
    thanks=["Happy to help","No worries"]
    bad_words = ["fuck", "Fuck", "dick","Dick"]
    if str(message.channel) in channels:
        if message.content.find("!hello") != -1:
            await message.channel.send(f"Hi there {message.author.name}, {random.choice(greetings)} !") 
            await message.channel.send(gif.gif_response('hello'))
        elif message.content == "!users":
            await message.channel.send(f"""This server has {guild_id.member_count} member(s)!""")
        elif message.content == (f"{client.user} How many Members does the server have?"):
            await message.channel.send(f"""This server has {guild_id.member_count} member(s)!""")
        elif message.content == "!thanks":
            await message.channel.send(f"{random.choice(thanks)} {message.author.name}")
            await message.channel.send(gif.gif_response('thanks'))         
    for word in bad_words:
        if message.content.count(word) > 0:
            await message.channel.purge(limit=1)
            await message.channel.send("Words like this are not permited in this server!")
    await client.process_commands(message)

@client.command() #Function to join the stock market 
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

@client.command() #Function to ask for a graph to show stock history 
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
    
@client.command() #Function to buy shares from stock market
async def buy(ctx,*,arg):
    if purchase.buy_stock(ctx.author.id,arg) == False:
        await ctx.send("Sorry, you can't buy this stock, you don't have enough money!")
    else:
        await ctx.send("Thanks for your purchase!")
        await ctx.send(gif.gif_response("empty wallet"))

@client.command() #Function to sell shares from curent owned ones
async def sell(ctx,*,arg):
    if selling.sell_stock(ctx.author.id,arg) == False:
        await ctx.send("Sorry, you can't sell this stock")
    else:
        await ctx.send("You have sold your stock(s)")
        await ctx.send(gif.gif_response("money"))
        
@client.command() #Shows the balance the user has
async def balance(ctx):
    wallet = db.get_user_balance(ctx.author.id)
    await ctx.send(f'You current balance is {wallet} USD')

@client.command() #View portfolio
async def portfolio(ctx):
    portfolio_dic = db.get_portfolio(ctx.author.id)
    temp_counter = 0
    portfolio_embed = discord.Embed(title ="Portfolio", description = "==============Stocks you own==============", color = 0x00ff00)



    for stock_listing in portfolio_dic:
        information_listing = "                  "
        

        for v in portfolio_dic[stock_listing].keys():

            print(v)

            if v== "total_shares":
                shares_have =  portfolio_dic[stock_listing]["total_shares"]

                removed_val = portfolio_dic[stock_listing].pop("total_shares")
                break
        information_listing += 'Total Shares:'+str(shares_have) +'\n'   
        information_listing += 'Total Shares Value:'+str(round(leaderboard.share_value(stock_listing)*shares_have,2)) +'\n'     
        for time_val in portfolio_dic[stock_listing]:
           
         #   information_listing += 'Total Shares:'+str(shares_have) +'\n'
        #    information_listing += 'Total Shares Value:'+str(round(leaderboard.share_value(stock_listing)*shares_have,2)) +'\n'

            #Total share value
            information_listing += '----------Date: '+time_val+'----------'+'\n'
            

            for hms_val in portfolio_dic[stock_listing][time_val]:
                information_listing += 'Time: '+hms_val+'\n\t\t'
                information_listing += "===============>"+ "  Price: "+ str(portfolio_dic[stock_listing][time_val][hms_val]['price'])+'\n\t\t\t'
                information_listing+="  ===============>"+ "   Shares: "+ str(portfolio_dic[stock_listing][time_val][hms_val]['shares'])+'\n\t\t\t'
        
        portfolio_embed.add_field(name=stock_listing, value=information_listing, inline= False) 
    await ctx.send(embed= portfolio_embed)

@client.command() #Explain financial terms
async def explain(ctx,term=None):
    financial = ["stock", "finance", "globalisation", "balance", "budget", "share", "equity"]
    if term == None:
        embed = discord.Embed(title ="Mr. Monopoly Help Menu", color = 0x9900FF)
        embed.add_field(name="How you should use the explain function.", value="Syntax: ```$explain <term>```")
        await ctx.send(embed=embed)
    elif term == "all":
        embed = discord.Embed(title ="Mr. Monopoly Explain Everything", color = 0x00ff00)
        embed.add_field(name="Explanation of stock", value="A stock (also known as shares or equity) is a type of security that signifies proportionate ownership in the issuing corporation. This entitles the stockholder to that proportion of the corporation's assets and earnings.", inline=False)
        embed.add_field(name="Explanation of finance", value="Finance is a term broadly describing the study and system of money, investments, and other financial instruments. Some authorities prefer to divide finance into three distinct categories: public finance, corporate finance, and personal finance. Other categories include the recently emerging area of social finance and behavioral finance, which seeks to identify the cognitive (e.g., emotional, social, and psychological) reasons behind financial decisions.", inline=False)
        embed.add_field(name="Explanation of globalisation", value="Globalization is the spread of products, technology, information, and jobs across national borders and cultures. In economic terms, it describes an interdependence of nations around the globe fostered through free trade.", inline=False)
        embed.add_field(name="Explanation of balance", value="An account balance is the amount of money present in a financial repository, such as a savings or checking account, at any given moment. The account balance is always the net amount after factoring in all debits and credits. An account balance that falls below zero represents a net debt—for example, when there is an overdraft on a checking account.", inline=False)
        embed.add_field(name="Explanation of budget", value="A budget is an estimation of revenue and expenses over a specified future period of time and is usually compiled and re-evaluated on a periodic basis. Budgets can be made for a person, a family, a group of people, a business, a government, a country, a multinational organization or just about anything else that makes and spends money. At companies and organizations, a budget is an internal tool used by management and is often not required for reporting by external parties.", inline=False)     
        await ctx.send(embed=embed)
    elif term in financial:
        embed = discord.Embed(color = 0x00ff00)
        if term == "stock" or "share" or "equity":
            embed.add_field(name="Explanation of stock", value="A stock (also known as shares or equity) is a type of security that signifies proportionate ownership in the issuing corporation. This entitles the stockholder to that proportion of the corporation's assets and earnings.", inline=False)
        elif term == "finance":
            embed.add_field(name="Explanation of finance", value="Finance is a term broadly describing the study and system of money, investments, and other financial instruments. Some authorities prefer to divide finance into three distinct categories: public finance, corporate finance, and personal finance. Other categories include the recently emerging area of social finance and behavioral finance, which seeks to identify the cognitive (e.g., emotional, social, and psychological) reasons behind financial decisions.", inline=False)
        elif term == "globalisation":
            embed.add_field(name="Explanation of globalisation", value="Globalization is the spread of products, technology, information, and jobs across national borders and cultures. In economic terms, it describes an interdependence of nations around the globe fostered through free trade.", inline=False)
        elif term == "balance":
            embed.add_field(name="Explanation of balance", value="An account balance is the amount of money present in a financial repository, such as a savings or checking account, at any given moment. The account balance is always the net amount after factoring in all debits and credits. An account balance that falls below zero represents a net debt—for example, when there is an overdraft on a checking account.", inline=False)
        elif term == "budget":
            embed.add_field(name="Explanation of budget", value="A budget is an estimation of revenue and expenses over a specified future period of time and is usually compiled and re-evaluated on a periodic basis. Budgets can be made for a person, a family, a group of people, a business, a government, a country, a multinational organization or just about anything else that makes and spends money. At companies and organizations, a budget is an internal tool used by management and is often not required for reporting by external parties.", inline=False)     
        await ctx.send(embed=embed)

    else:
        await ctx.send("Term not present in the dictionary")

@client.command() #Clear (purge) messages from channel (can only be used by users with administrator permissions)
async def clear(ctx, ammount=100):
    channel = ctx.message.channel
    if ctx.message.author.guild_permissions.administrator:
        await channel.purge(limit=ammount,check=None,bulk=True)
    else:
        await ctx.send("You can't use that command, you are not an administrator!")



@client.command()# $predict [userInput]
async def predict(ctx,*,arg):
    prediction = model_query.evaluate_model(arg)
    await ctx.send(prediction)

"""
@client.command()# $predict [userInput]
async def leaderboards(ctx):
    embed = discord.Embed(title ="Leaderboard", color = 0x9900FF)
    for person in leaderboard.leaderboardList():
        embed.add_field(name=str(person[0])+' '+str(person[1])+' net worth is $'+str(person[2]), value="Total stocks owned:"+str(leaderboard.total_shares_user(person[3])), inline=False)
    await ctx.send(embed=embed)
"""
client.run(token)