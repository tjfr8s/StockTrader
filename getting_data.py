import quandl
quandl.ApiConfig.api_key = "Z5F88HqyZ_2ApQUK9cMc"
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web


style.use('ggplot')

start = dt.datetime(2000,1,1)
end = dt.datetime(2018,7,30)

df = web.DataReader('TSLA', 'quandl', start, end)

print(df.tail(6))
