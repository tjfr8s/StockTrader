import quandl
## doesn't work with current version of pandas_datareader,
## must set envrionment variable QUANDL_API_KEY instead
## quandl.ApiConfig.api_key = "Z5F88HqyZ_2ApQUK9cMc"

import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates

## Create dataframe contining stock information using quantl API
##style.use('ggplot')
##start = dt.datetime(2015,1, 1)
##end = dt.datetime.now()
##df = web.DataReader("TSLA", 'quandl', start, end)
##df.to_csv('tsla.csv')

df = pd.read_csv('tsla.csv', parse_dates = True, index_col = 0)
df.drop(["AdjOpen", "ExDividend", "SplitRatio", "AdjHigh",
         "AdjVolume"], axis = 1, inplace = True)

#### Calculate 100 moving average and add to dataframe
#### Create subplots plot various parts of data
##df['100ma'] = df['AdjClose'].rolling(window=100, min_periods=0).mean()
##print(df.head())
##





## OHLC data creation
df_ohlc = df['AdjClose'].resample('10D').ohlc()
df_volume = df['Volume'].resample('10D').sum()

df_ohlc.reset_index(inplace = True)

# Convert dates to mdates for use with matplotlib
df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)


ax1 = plt.subplot2grid((6, 1), (0,0), rowspan = 5, colspan = 1)
ax2 = plt.subplot2grid((6, 1), (5,0), rowspan = 1, colspan = 1, sharex = ax1)
ax1.xaxis_date()

candlestick_ohlc(ax1, df_ohlc.values, width = 2, colorup = 'g')
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
plt.show()
