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
    high_low = df["high"] - df["low"]
    high_close = np.abs(df["high"] - df["close"].shift())
    low_close = np.abs(df["low"] - df["close"].shift())

    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)

    atr = true_range.rolling(14).sum() / 14
    df["atr"] = atr
    df.dropna(subset=["atr"], inplace=True)
    return df


def process_symbol(symbol):
    daily = api.get_bars(symbol, TimeFrame.Day, start, end, adjustment="raw").df
    daily["date"] = daily.apply(lambda row: to_date(row), axis=1)
    daily = daily.set_index("date")
    for date in daily.index.tolist():
        fifteen = api.get_bars(
            symbol, TimeFrame.Fifteen, date, date, adjustment="raw"
        ).df
        # Remove pre-market
        fifteen = fifteen.loc[fifteen.index.time >= datetime.time(14, 30)]
        # Remove post-market
        fifteen = fifteen.loc[fifteen.index.time <= datetime.time(20, 45)]
        daily.loc[date, "15min_close"] = fifteen.iloc[0].close
        daily.loc[date, "is_positive_start"] = bool(
            fifteen.iloc[0].close > fifteen.iloc[0].open
        )
        daily.loc[date, "is_positive_end"] = bool(
            fifteen.iloc[0].close < daily.loc[date].close
        )
        daily.loc[date, "15min_volume"] = fifteen.iloc[0].volume
    daily = add_atr(daily)
    with open("{}.1000.csv".format(symbol), "w") as fp:
        daily.to_csv(fp)


end = datetime.date.today().isoformat()
start = (datetime.date.today() - datetime.timedelta(days=1000)).isoformat()
api = alpaca()
