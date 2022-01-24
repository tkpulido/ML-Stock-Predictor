from datapoller import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score


def train_and_plot(symbol, verbose=False):
    # Fetch the time series. Compute the required data fields and store it in CSV
    process_symbol(symbol)
    
    # Open the CSV created earlier and store the data
    with open("{}.1000.csv".format(symbol), "r") as fp:
        df = pd.read_csv(fp)
    
    # add the new ATR field
    df = add_atr(df)
    
    # Compute the X matrix with 3 inputs. Open Price, FIrst 15 Min candle is green (True) or Red(False), ATR
    X = df[["open", "is_positive_start", "atr"]].values.reshape(-1, 3)
    # Load the Y values. Close price of the day. This is what we are going to predict.
    y = df[["close"]].values.reshape(-1, 1)
    
    # Split the X data to to training data and test data. 50 days of test data. Remaining is training data.
    X_train = X[:-50]
    X_test = X[-50:]
    
     # Split the Y data to to training data and test data. 50 days of test data. Remaining is training data.
    y_train = y[:-50]
    y_test = y[-50:]
    
    # create a Linear regression model
    regr = linear_model.LinearRegression()
    
    # train the data.
    regr.fit(X_train, y_train)

    # Do the prediction on the test data
    y_pred = regr.predict(X_test)
    
    # Print the wieghts assigned by the model.
    print("Coefficients: \n", regr.coef_)

    # Get the X-axis for the test data.
    d = df["date"][-50:]
    
    # Set the size of the plit
    plt.rcParams["figure.figsize"]=30,8
    plt.scatter(d, y_test, color="black")
    plt.plot(d, y_pred, color="blue", linewidth=1)
    plt.xticks(rotation=90)
    plt.legend(["Actual", "predicted"])
    plt.title("{}".format(symbol))
    plt.xticks(rotation=90)
    
    # Verbose mode: label the data points as well.
    if (verbose == True):
        for i, txt in enumerate(y_test.reshape(-1, 50)[0]):
            plt.annotate(txt, (d.iloc[i], y_test[i] - 0.5))
        for i, txt in enumerate(y_pred.round(2).reshape(-1, 50)[0]):
            plt.annotate(txt, (d.iloc[i], y_test[i] + 0.5), color="blue")

    # Save output to file
    #plt.savefig("{}.png".format(symbol))
    
    # Plot the output to screen
    plt.show()
    
    # Also print the score.
    print(regr.score(X_test, y_test))