import json
import requests
import matplotlib.pyplot as plt
from datetime import datetime
import sys
sys.path.insert(0, 'C:\\Users\\Dave.Wood\\Python')
from TemporalFeatures import Features as tp

api_key = 'AR1SDJXUBFO9GA6P'
api_url_base = 'https://www.alphavantage.co/query?'

def get_time_series_daily(function, symbol, outputsize, datatype):
    api_url = api_url_base+function+'&'+symbol+'&'+outputsize+'&'+datatype+'&'+'apikey='+api_key
    print(api_url)
    response = requests.get(api_url)
    
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

data = get_time_series_daily('function=TIME_SERIES_INTRADAY', 
                             'symbol=AMZN',
                             'outputsize=full',
                             'datatype=json')
time_price = [datetime.strptime(i, '%Y-%m-%d') for i in list(data['Time Series (Daily)'].keys())]    
open_price = [float(i['1. open']) for i in list(data['Time Series (Daily)'].values())] 
high_price = [float(i['2. high']) for i in list(data['Time Series (Daily)'].values())]    
low_price = [float(i['3. low']) for i in list(data['Time Series (Daily)'].values())]    
close_price = [float(i['4. close']) for i in list(data['Time Series (Daily)'].values())]    

open_resistance = tp.resistance(open_price , 60)
open_support = tp.support(open_price , 60)

plt.plot(time_price, open_price, color='blue')
plt.plot(time_price, open_resistance, color='magenta')
plt.plot(time_price, open_support, color='green')



