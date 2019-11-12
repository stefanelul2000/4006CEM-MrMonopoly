#TODO Get all users

# TODO user networth

import db as databseCommand
import requests
import datetime
from alpha_vantage.timeseries import TimeSeries as ts
from alpha_vantage.techindicators import TechIndicators
import analyse_text
import graph 


def leaderboardList():
    memberID_list= databseCommand.list_of_members()
    print('ids:',memberID_list)
    leaderboardList = [['rank','a',10000],['rank','b',100]]# [[rank,name,networth]]

    for memberID in memberID_list:
        schema_leaderboard=(["rank",databseCommand.get_name(memberID),net_worth(memberID)])
        print(schema_leaderboard)
        leaderboardList.append(schema_leaderboard)

    
    leaderboardList = sorted(leaderboardList, key = lambda x: x[2])

 #   print(leaderboardList)
    leaderboardList.reverse()
#
  #  print(leaderboardList)

    for i in range(len(leaderboardList)):
       # print(i)
        leaderboardList[i][0] = i+1
    
    
    return leaderboardList



def net_value_of_stocks(userID):
    
    total_share_value = 0
    portfolio = databseCommand.get_portfolio(userID)
    print(portfolio)
    for stocks in portfolio:
        total_shares  = portfolio[stocks]["total_shares"]
        total_share_value += share_value(stocks) * total_shares
        
    
    return round(total_share_value,2)




def total_shares_user(userID):
    total_shares_user = 0
    portfolio = databseCommand.get_portfolio(userID)
    print(portfolio)
    for stocks in portfolio:
        total_shares  = portfolio[stocks]["total_shares"]
        total_shares_user += total_shares

    return total_shares_user


def net_worth(userID):
   balance = databseCommand.get_user_balance(userID)
   #print('balance',balance,'userID',userID) 
   worth = balance  + net_value_of_stocks(userID)

   return round(worth,2)





def share_value(ticker):
    API_KEY = graph.generate_api_key()
    r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ticker+'&outputsize=full&apikey=' + API_KEY)
    results = r.json()
    for day in results['Time Series (Daily)']:
        worth = float(results['Time Series (Daily)'][day]['4. close'])
        break

    print(ticker,worth)

    return round(worth,2) 




#print(stock_net_value(267402605318242304))


print(leaderboardList())

    # closing_list = []
    # dates = []

    # days_get = days
    # count = 0

    # for day in results['Time Series (Daily)']:
        
    #     if count == days_get:
    #             break
    #     dt = datetime.datetime.strptime(day, '%Y-%m-%d').strftime('%d/%m')
    #     dates.append(dt)
    #    # dates.append(day)
        # closing_list.append(float(results['Time Series (Daily)'][day]['4. close']))
        
       # count += 1
    # dates.reverse()
    # closing_list.reverse()
    # return dates,closing_list