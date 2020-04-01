import numpy as np
import matplotlib.pyplot as plt
from binance.client import Client
import time
import sys
import tensorflow
from keras.layers import Dense
from keras.models import Sequential
from keras import optimizers
sys.path.insert(0, 'C:\\Users\\dwood\\Python')
from TemporalFeatures import Features as tp

#----------------------------------------------------------------------------------#
np.random.seed(seed=7)

api_key = 'EdZbJVPs0BmKaDQWr4lw0EXT6deDKcubL9W7Mc66xDLXa2xC78t09PpfLeYY0d4x'
api_secret = 'BG6UffLixG83BdmqwObfuzAVSlhCQBqFBAMFIOQHIphkmBS2CT2qAQcYWFCvy22S'
client = Client(api_key, api_secret)

token = 'BTC'
asset = 'USDT'
data_days = 365  #Days

#----------------------------------------------------------------------------------#
pretime = time.time()
klines = client.get_historical_klines(token+asset, Client.KLINE_INTERVAL_1MINUTE,
                                      str(time.time()-(86400*data_days)))

open_price = list([float(i[1]) for i in klines])

print(str(time.time() - pretime))

high_price = list([float(i[2]) for i in klines])
low_price = list([float(i[3]) for i in klines])
close_price = list([float(i[4]) for i in klines])
volume = list([float(i[5]) for i in klines])
quote_asset_volume = list([float(i[7]) for i in klines])
number_of_trades = list([float(i[8]) for i in klines])
taker_buy_base_asset_volume =  list([float(i[9]) for i in klines])
taker_buy_quote_asset_volume = list([float(i[10]) for i in klines])
open_time = list([float(i[0]) for i in klines])
close_time = list([float(i[6]) for i in klines])

#----------------------------------------------------------------------------------#
pretime = time.time()
klines = client.get_historical_klines(token+asset, Client.KLINE_INTERVAL_1MINUTE,
                                      str(time.time()-(86400*data_days)))

open_price = list([float(i[1]) for i in klines])

print(str(time.time() - pretime))

for j in range(1, 61):
    return_sweep = []
    exchange_sweep = []  
    long_interval = 1440*7*52
    timeNOW = time.time();
    #int_min = tp.moving_min(open_price, long_interval)
    int_max = tp.moving_max(open_price, long_interval)
    print(str(time.time() - timeNOW));
    
    mov_avg = tp.moving_average(open_price, 1440*30)
    res_01 = tp.resistance(open_price, 1440*30)
    sup_01 = tp.support(open_price, 1440*30)
    res_trend = tp.resistance_trendline(open_price, 2880, 0.6)
    sup_trend = tp.support_trendline(open_price, 2880, 0.6)
    mov_dx = tp.derivative_ratio(open_price, 10)
    second_diff = tp.average_difference_percent(open_price, 2, 1440)
     
    print(str(time.time() - timeNOW));
    
    for i in range(0, 101):        
        exchange_fee = 0.001
        risk_coeff = i/100
        
        funds = 10000
        funds_list = [funds]
        tokens = 0
        tokens_list = [(funds+tokens*open_price[0])] 
        value_list = [(funds, True)]
        
        exchange_price = []
        
        buy_val = 0
        sell_val = 0
        
        good_exchange_counter = 0
        bad_exchange_counter = 0        
                
        for x in range(1, len(open_price)):
            current_price = open_price[x]
            
            fund_check = int(funds*risk_coeff*100)/100
            token_sell = int(tokens*risk_coeff*100)/100
            
            token_buy = int((funds/current_price)*risk_coeff*100)/100
            value_check = int(risk_coeff*current_price*tokens*100)/100
            
            if(((current_price > res_01[x])            
                    ) and         
                    (fund_check > 10)): 
                buybool = True                       
                tokens = tokens + (1-exchange_fee)*token_buy                
                funds = funds - current_price*token_buy        
            elif(((current_price < sup_01[x])
                    ) and 
                    (value_check > 10)):   
                buybool = False                
                funds = funds + (1-exchange_fee)*current_price*token_sell                
                tokens = tokens - risk_coeff*tokens       
            else:
                funds_list.append(funds)
                tokens_list.append(tokens)         
            if((funds+tokens*current_price)/value_list[x-1][0] == 1):
                value_list.append((funds+tokens*current_price, True))            
            else:
                value_list.append((funds+tokens*current_price, False))            
        print(str(i) +
              ": return = : " + 
              str(value_list[-1][0]/value_list[0][0]) +
              ", Funds: " + 
              str(funds) + 
              ", Tokens: " + 
              str(tokens))          
        return_sweep.append(value_list[-1]/value_list[0])        
       
#----------------------------------------------------------------------------------#
# Plotting and Visualization        
plt.plot(return_sweep)
plt.plot(exchange_sweep)
plt.plot(li)

plt.plot(open_price, color='orange')
plt.plot(tp.normalize(open_price), color='orange')
plt.plot(int_max, color='blue')
plt.plot(int_min, color='red')
plt.plot(tp.normalize([x[0] for x in value_list[:]]), color='black')

plt.plot(res_01, color='green')
plt.plot(sup_01, color='magenta')

#----------------------------------------------------------------------------------#

interval_length = 72
interval_prediction = 1
y = [open_price[t-interval_length:t] for t in range(interval_length+interval_prediction, len(open_price), interval_prediction)]
x = [open_price[t-interval_length:t] for t in range(interval_length, len(open_price)-interval_prediction, interval_prediction)]

training_split = int(np.floor(len(x)*0.7))
x_train = x[0:training_split]
x_test = x[training_split:len(x)]
y_train = y[0:training_split]
y_test = y[training_split:len(x)]

model = Sequential()
for i in range(10):
    model.add(Dense(interval_length, activation='relu', use_bias=True))
    model.add(Dropout(0.25))

model.compile(loss='mse', optimizer=optimizers.adam(lr = 0.0001)) 
model.fit(x_train, y_train, validation_split=0.33, epochs=40, batch_size=(100), verbose=2, shuffle = False)