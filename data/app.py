from datapoller import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score


def train_and_plot(symbol):
    process_symbol(symbol)
    with open("{}.1000.csv".format(symbol), "r") as fp:
        df = pd.read_csv(fp)
    df = add_atr(df)
    X = df[["open", "is_positive_start", "atr"]].values.reshape(-1, 3)
    y = df[["close"]].values.reshape(-1, 1)
    X_train = X[:-50]
    X_test = X[-50:]
    y_train = y[:-50]
    y_test = y[-50:]
    regr = linear_model.LinearRegression()
    # regr.fit(X_train, y_train)
    regr.fit(X, y)

    y_pred = regr.predict(X_test)
    print("Coefficients: \n", regr.coef_)

    d = df["date"][-50:]
    # plt.rcParams["figure.figsize"]=30,8
    plt.scatter(d, y_test, color="black")
    plt.plot(d, y_pred, color="blue", linewidth=1)
    plt.xticks(rotation=90)
    plt.legend(["Actual", "predicted"])
    plt.title("{}".format(symbol))
    plt.xticks(rotation=90)
    for i, txt in enumerate(y_test.reshape(-1, 50)[0]):
        plt.annotate(txt, (d.iloc[i], y_test[i] - 0.5))
    for i, txt in enumerate(y_pred.round(2).reshape(-1, 50)[0]):
        plt.annotate(txt, (d.iloc[i], y_test[i] + 0.5), color="blue")
    plt.show()
    print(regr.score(X_test, y_test))
