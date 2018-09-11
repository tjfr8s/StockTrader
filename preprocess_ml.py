import numpy as np
import pandas as pd
import pickle

def process_data_for_labels(ticker):
    hm_days = 7
    # create df from sp500 data csv
    df = pd.read_csv('sp500_joined_closes.csv', index_col=0)

    # compile list of tickers from column headers of df
    tickers = df.columns.values.tolist()
    df.fillna(0, inplace=True)

    # create mh_days columns for percent change in price over that many days
    for i in range(1, hm_days+1):
        df['{}_{}d'.format(ticker, i)] = (df[ticker].shift(-i) - df[ticker]) / df[ticker]

        df.fillna(0,inplace=True)
        return tickers, df


def buy_sell_hold(*args):
    cols = [c for c in args]
    requirement = 0.02

    # determine whether to buy, sell, or hold based on percent change price data
    for col in cols:
        if col > requirement:
            return 1
        if col < -requirement:
            return -1
    return 0










































