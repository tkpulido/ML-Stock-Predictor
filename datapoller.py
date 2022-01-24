from alpaca_trade_api.rest import REST, TimeFrame
import os
import datetime
import numpy as np
import pandas as pd


def alpaca():
    return REST(
        base_url="https://paper-api.alpaca.markets",
        secret_key=os.environ.get("APCA_API_SECRET_KEY"),
        key_id=os.environ.get("APCA_API_KEY_ID"),
    )


def to_date(row):
    return row.name.date().isoformat()


def add_atr(df):
    # Compute ATR of the data frame based on ohlc time series.
    high_low = df["high"] - df["low"]
    high_close = np.abs(df["high"] - df["close"].shift())
    low_close = np.abs(df["low"] - df["close"].shift())

    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)

    # 14 SMA
    atr = true_range.rolling(14).sum() / 14
    df["atr"] = atr
    df.dropna(subset=["atr"], inplace=True)
    return df


def process_symbol(symbol):
    # Fetch Daily for the last 1000 Days.
    daily = api.get_bars(symbol, TimeFrame.Day, start, end, adjustment="raw").df
    
    # Convert date from timestamp to isoformat
    daily["date"] = daily.apply(lambda row: to_date(row), axis=1)
    
    # Use data as index
    daily = daily.set_index("date")
    
    for date in daily.index.tolist():
        # For each date, fetch the 15 Min candles. *** Heavy API usage ***
        fifteen = api.get_bars(
            symbol, TimeFrame.Fifteen, date, date, adjustment="raw"
        ).df
        
        # Remove pre-market
        fifteen = fifteen.loc[fifteen.index.time >= datetime.time(14, 30)]
        
        # Remove post-market
        fifteen = fifteen.loc[fifteen.index.time <= datetime.time(20, 45)]
        
        # save 15 Min close of the first 15 min.
        daily.loc[date, "15min_close"] = fifteen.iloc[0].close
        
        # compute first 15 min is +ve or -ve
        daily.loc[date, "is_positive_start"] = bool(
            fifteen.iloc[0].close > fifteen.iloc[0].open
        )
        # compute if the day ended +ve or -ve
        daily.loc[date, "is_positive_end"] = bool(
            fifteen.iloc[0].close < daily.loc[date].close
        )
        # Also include 15Min voumne
        daily.loc[date, "15min_volume"] = fifteen.iloc[0].volume
    # Add ATR attribute
    daily = add_atr(daily)
    # Save everything to file
    with open("{}.1000.csv".format(symbol), "w") as fp:
        daily.to_csv(fp)

# Init start and end dates
end = datetime.date.today().isoformat()
start = (datetime.date.today() - datetime.timedelta(days=1000)).isoformat()

# Create connection with broker
api = alpaca()