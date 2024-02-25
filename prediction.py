from datetime import timedelta

import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.simplefilter("ignore")

info = pd.read_csv('data.csv')
dates = info.set_index('day',inplace=True)
dates = pd.to_datetime(info.index)
cashback = info.set_index('cashback',inplace=True)
cashback = info.index
company = info.set_index('merchant_name',inplace=True)
company = info.index

csh_dt = pd.DataFrame({'merchant_name':company,'day':dates,'cashback':cashback})
csh_dt.dropna(inplace=True)
split_db = list()

temp_name = csh_dt.values[0][0]
last_i = 0
for i in range(len(csh_dt.values)):
    if temp_name != csh_dt.values[i][0]:
        temp_name = csh_dt.values[i][0]
        split_db.append(pd.DataFrame({'merchant_name':company[last_i:i],'day':(dates[last_i:i]),'month':'2023-02-01 00:00:00','cashback':cashback[last_i:i]}))
        last_i = i
split_db.append(pd.DataFrame({'merchant_name':company[last_i:i+1],'day':(dates[last_i:i+1]),'month':'2023-02-01 00:00:00','cashback':cashback[last_i:i+1]}))

cmb = [(4,0,4),(3,1,3),(3,0,2),(5,0,1),(3,1,3),(4,1,4),(5,0,1),(3,0,1),(3,0,1),(5,0,1)]
names = ['5КармаNoв','Bonafide','Globus','PREMIER','Vprok.ru Перекрёсток','Много лосося','Пятерочка','Ситидрайв','Столото','Читай-город']
f = open('itog2.csv', 'w')
f.write('merchant_name,day,month,cashback\n')
f.close()
for i in range(10):
    n = 28 - split_db[i]['day'][len(split_db[i]['day'])-1].day
    model = ARIMA(split_db[i]['cashback'], order=cmb[i])
    model_fit = model.fit()
    forecast_future = model_fit.forecast(steps=n)
    future_dates = pd.date_range(start=(split_db[i]['day'][len(split_db[i]['day'])-1]+timedelta(days=1)), periods=n, freq='D')
    forecast_df = pd.DataFrame({'merchant_name':names[i],'day': future_dates.strftime("%Y-%m-%d %H:%M:%S"),'month': '2023-02-01 00:00:00', 'cashback': forecast_future})
    split_db[i].to_csv('itog2.csv', mode='a', encoding='utf-8',index=False,header=None)
    forecast_df.to_csv('itog2.csv', mode='a',encoding='utf-8',index=False,header=None)
print('Success')
