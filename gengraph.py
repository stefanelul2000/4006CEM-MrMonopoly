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
#import pandas as pd



def generate_api_key():
    api_key_list = ['QGXU2BPYW3O6BZ1M','OIANPZYCJ7CPJJPR',' MLPELGS77KBUFETO','BC05ZA0TDMYJMJ5F']

    return random.choice(api_key_list)



def closing_info(ticker='GOOG',time_scale=5):
    API_KEY = generate_api_key()
    r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ticker+'&apikey=' + API_KEY)
    results = r.json()



    closing_list = []
    dates = []

    days_get = time_scale
    count = 0

    for day in results['Time Series (Daily)']:
        
        if count == days_get:
                break
        dates.append(day)
        closing_list.append(float(results['Time Series (Daily)'][day]['4. close']))
        
        count += 1
    dates.reverse()
    closing_list.reverse()
    return dates,closing_list



def information_type(info,time_scale,ticker):

    if info == "close" or "closing":

        axis_x ,axis_y = closing_info(ticker,time_scale)
        graphcompany(axis_x,axis_y)


def graphcompany(axis_x,axis_y):
##if checkCompany(gCompany)==True:
   
  
    
  

    plt.plot(axis_x,axis_y, linestyle='--', marker='o', color='b')
    plt.grid(True)
    plt.ylabel('Price per stock of in USD')
    plt.xlabel('Past 5 days')
    plt.savefig('stockImage.png')
    plt.show()

            #
            # parsed_json[day] = day["4. close"]

   # print( parsed_json)

    


  #  for i in range(8):


 #   print(results)
   # if (r.status_code == 200):
    #    result = r.json()
        #allDaysData = result['Time Series (Daily)']
       # i = 0
       # print(allDaysData)


#egGraph()
#information_type("close",5,'AMZN')

"""       
        while i < 6:
            iDayData = (allDaysData[(datetime.datetime.now() - datetime.timedelta(days=i)).date().strftime('%Y-%m-%d')]
            dayDataList[i] =iDayData['1. open'] 
            i = i+1


        plt.plot([0,1,2,3,4,5,6],iDayData)

        

"""
#def checkCompany(gCompany)
    ##if gcompany in dictionary of all stock company abbreviations then 
    ##return True
    ##else
    ##return False






'''

from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt

ts = TimeSeries(key='YOUR_API_KEY', output_format='pandas')
data, meta_data = ts.get_intraday(symbol='MSFT',interval='1min', outputsize='full')
data['4. close'].plot()
plt.title('Intraday Times Series for the MSFT stock (1 min)')
plt.show()


'''