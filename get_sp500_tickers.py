import bs4 as bs
import quandl
import datetime as dt
import os
import numpy as np
import pandas as pd
import pandas_datareader.data as web
import pickle
import requests
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')

def save_sp500_tickers():
    """Get list of sp500 tickers from wikipedia using beautiful soup"""

    ## Get source code of sp500 wikipedia page 
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find('table', {'class' :  'wikitable sortable'})
    tickers = []

    ## parse wikipedia source code for tickers and add them to list of tickers
    for row in table.findAll('tr') [1:] :
        ticker = row.findAll('td') [0].text
##        if "." in ticker:
##            ticker = ticker.replace(".", "-")
        tickers.append(ticker)

    ## save ticker list using pickle
    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)

    print(tickers)
    return tickers


def get_data_from_api(reload_sp500 = False):
    """ get and save ticker data for all tickers in
    list of tickers """
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        ## load saved data as pickle object
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)

    ## create directory and store ticker data in it
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    ## save each collection ticker data as tickername.csv if
    ## that file doesn't already exist
    start = dt.datetime(2014, 1, 1)
    end = dt.datetime(2017, 12, 31)

    for ticker in tickers:
        print(ticker)
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = web.DataReader(ticker, 'iex', start, end)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))

def compile_data():
    """ combines close prices of each ticker in sp500 into
    single dataframe"""

    # Open and load ticker names
    with open("sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame()

    for count, ticker in enumerate(tickers):
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
        df.set_index('date', inplace = True)

        df.rename(columns = {'close': ticker}, inplace=True)
        df.drop(['open', 'high', 'low',  'volume'], 1, inplace=True)

        if main_df.empty:
            main_df = df
            
        else:
            main_df = main_df.join(df, how='outer')

        print(ticker)

    print(main_df.head())
    main_df.to_csv('sp500_joined_closes.csv')


def visualize_data():
    df = pd.read_csv('sp500_joined_closes.csv')
##    df['AAPL'].plot()
##    plt.show()
    df_corr = df.corr()

    print(df_corr.head(15))
    data = df_corr.values
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn)
    fig.colorbar(heatmap)

    ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
    ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)

    ax.invert_yaxis()
    ax.xaxis.tick_top()

    column_labels = df_corr.columns
    row_labels = df_corr.index

    ax.set_xticklabels(column_labels)
    ax.set_yticklabels(row_labels)
    plt.xticks(rotation = 90)
    heatmap.set_clim(-1, 1)
    plt.tight_layout()
    plt.show()
    

#save_sp500_tickers()
#get_data_from_api(True)
#compile_data()
visualize_data()
    

