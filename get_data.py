import quandl
quandl.ApiConfig.api_key = "Z5F88HqyZ_2ApQUK9cMc"
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

## Create dataframe contining stock information using quantl API
##style.use('ggplot')
##start = dt.datetime(2015,1, 1)
##end = dt.datetime.now()
##df = web.DataReader("TSLA", 'quandl', start, end)
##df.to_csv('tsla.csv')

df = pd.read_csv('tsla.csv', parse_dates = True, index_col = 0)
df.drop(["AdjOpen", "ExDividend", "SplitRatio", "AdjHigh",
         "AdjVolume"], axis = 1, inplace = True)
df['100ma'] = df['AdjClose'].rolling(window=100, min_periods=0).mean()
print(df.head())

ax1 = plt.subplot2grid((6, 1), (0,0), rowspan = 5, colspan = 1)
ax2 = plt.subplot2grid((6, 1), (5,0), rowspan = 1, colspan = 1, sharex = ax1)

ax1.plot(df.index, df['AdjClose'])
ax1.plot(df.index, df['100ma'])
ax2.bar(df.index, df['Volume'])

plt.show()
