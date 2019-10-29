##pip install alpha_vantage
##pip install matplotlib
##pip install requests
import requests
import datetime
from alpha_vantage.timeseries import TimeSeries as ts
from alpha_vantage.techindicators import TechIndicators
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
import random
import os
import analyse_text
import numpy as np
import matplotlib.dates 
#fig2 = plt.pyplot.figure(figsize=(8.0, 5.0))







"""
========
Read me:
=========
Dependicies to install:

pip install alpha_vantage
pip install matplotlib
pip install requests



================

METHOD
~~~~~~~~~~~~~~~~~
information_type(info_wanted,time_scale,days,company_name)
~~~~~~~~~~~~~~~~~

-Pass string, string, int, string

-Returns graph by creating stockImage.png

################Important##################

FIRST PARAMETER: info_wanted MUST BE 'close'

###########################################

- E.g 

#information_type(info_wanted,time_scale,days,company_name)

>>>>>>>information_type("close","week",5,"google")


############Important#############

To get time_scale , days , company name

YOU NEED TO USE THE analyse_text.py METHODS!

###########################################
- To implement in Discord bot:

1. User does @wallstreetbot Show me the last 5 days of Apple stocks

2. Get user input and store as variable

3. Pass user input to analyse_text.py by importing the file

3a. Make sure you have read the doucmentation 

4. Get the OUTPUT of analyse_text.py and carefully plug into this files method 
information_type(info_wanted,time_scale,days,company_name)

5. stockImage.png is generated, send that file to Discord channel

6. ??????

7. Profit

"""





def company_name_converter(company_name):
   company_name = company_name.lower() 
   #company_name = company_name.replace('inc', '')

  # company_name = company_name.strip('inc')
  # print(company_name)
   stockDict = {"apple":"AAPL","alphabet":"GOOGL","microsoft":"MSFT","amazon":"AMZN","facebook":"FB","google":"GOOGL","apple inc":"AAPL", "amazon inc": "AMZN"}

   if company_name in stockDict:
       return stockDict[company_name]
    
   else:
        print('not in dic')


def generate_api_key():
    api_key_list = ['QGXU2BPYW3O6BZ1M','OIANPZYCJ7CPJJPR',' MLPELGS77KBUFETO','BC05ZA0TDMYJMJ5F']
    
    

    return random.choice(api_key_list)



def closing_info(ticker='GOOG',days=5):
    API_KEY = generate_api_key()
    r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ticker+'&outputsize=full&apikey=' + API_KEY)
    results = r.json()



    closing_list = []
    dates = []

    days_get = days
    count = 0

    for day in results['Time Series (Daily)']:
        
        if count == days_get:
                break
        dt = datetime.datetime.strptime(day, '%Y-%m-%d').strftime('%d/%m')
        dates.append(dt)
       # dates.append(day)
        closing_list.append(float(results['Time Series (Daily)'][day]['4. close']))
        
        count += 1
    dates.reverse()
    closing_list.reverse()
    return dates,closing_list






###############################################
def information_type(info_wanted,time_scale,days,company_name):

    if info_wanted == "close" or "closing":
        ticker = company_name_converter(company_name)
        axis_x ,axis_y = closing_info(ticker,days)
        graphcompany(axis_x,axis_y,days,ticker)
###############################################

def graphcompany(axis_x,axis_y,days,company_name):

    days_shown = str(days)
    companyTitle = str(company_name)
    plt.style.use('ggplot')
    #plt.xkcd()
  
    
  
    
    figure = plt.gcf() # get current figure
   # figure.set_size_inches(8, 6)

    fig, ax = plt.subplots()
    




 

    plt.xticks(rotation=45)


 
    plt.plot(axis_x,axis_y,linestyle='--', color='b')
 
    if days> 14 and days < 41:
        every_nth = 2
    
    if days> 41 and days < 95:
        every_nth = 5

    if days> 95 and days <= 200:
        every_nth = 10

    if days> 200 and days < 400:
        every_nth = 15

    else:
        every_nth = 1

    
    if days> 250:
        days = 250

    for n, label in enumerate(ax.xaxis.get_ticklabels()):
                if n % every_nth != 0:
                        label.set_visible(False)


   
    plt.grid(True)
    plt.ylabel('Price in USD')
    plt.xlabel('Past '+days_shown+' day(s)')
    
    plt.gcf().subplots_adjust(bottom=0.17)
    
    plt.title(companyTitle+" stock performance")


    
  #  if os.path.exists("stockImage.png"):
    #    os.remove("stockImage.png")

    plt.savefig('stockImage.png',dpi =512)
    #plt.show()

        







#information_type(info_wanted,time_scale,days,company_name)

#information_type(info_wanted = 'close',time_scale="week",days=5 ,company_name='google')

#TODO Get Time period, E.g from 3 years ago to today