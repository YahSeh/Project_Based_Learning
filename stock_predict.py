import csv
import numpy as np
from sklearn.svm import SVR
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime, timedelta
import warnings
from sklearn.exceptions import DataConversionWarning
import time

warnings.simplefilter("ignore", category=FutureWarning)
warnings.simplefilter("ignore", category=DataConversionWarning)

def get_data(ticker):
    end = datetime.now()
    start = end - timedelta(days=timespan)
    data = yf.download(ticker, start=start, end=end)

    dates = []
    prices = []

    for i, date in enumerate(data.index):
        dates.append(i) # Index used as x-values
        prices.append(data['Close'].iloc[i])

    return np.array(dates), np.array(prices)

def predict_prices(dates, prices, x, ticker):
    dates = np.reshape(dates, (len(dates), 1))

    svr_lin = SVR(kernel='linear', C=1e3)
    svr_poly = SVR(kernel='poly', C=1e3, degree=2)
    svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
    
    svr_lin.fit(dates, prices)
    svr_poly.fit(dates, prices)
    svr_rbf.fit(dates, prices)

    # Predict actual data and models
    future_days = np.array([[x + i] for i in range(1, (nextdays+1))])  # x is len(dates)
    pred_rbf = svr_rbf.predict(future_days)
    pred_lin = svr_lin.predict(future_days)
    pred_poly = svr_poly.predict(future_days)

    # Resize Figures
    plt.figure(figsize=(len(dates) * 0.5, 6))

    # Plot actual data and models
    plt.scatter(dates, prices, color='black', label='Actual Data')
    
    # RBF Prediction
    plt.plot(dates, svr_rbf.predict(dates), color='red', label='RBF model')
    # Linear Prediction
    plt.plot(dates, svr_lin.predict(dates), color='green', label='Linear model')
    # Polynomial Prediction
    plt.plot(dates, svr_poly.predict(dates), color='blue', label='Polynomial model')
    
    # Plot predictions
    for i in range(3):
        day = x + i + 1  # Future index
        plt.scatter(day, pred_rbf[i], color='red', marker='x', s=100)
        plt.text(day + 1, pred_rbf[i], f"{pred_rbf[i]:.2f}", color='red')

        plt.scatter(day, pred_lin[i], color='green', marker='x', s=100)
        plt.text(day + 1, pred_lin[i], f"{pred_lin[i]:.2f}", color='green')

        plt.scatter(day, pred_poly[i], color='blue', marker='x', s=100)
        plt.text(day + 1, pred_poly[i], f"{pred_poly[i]:.2f}", color='blue')

    plt.xlabel('Trading-day Index')
    plt.ylabel('Price')
    plt.title(f"{ticker} Price last {timespan} days (last {len(dates)} trading days)")
    plt.legend()
    plt.tight_layout()
    plt.show(block=False)

    return pred_rbf, pred_lin, pred_poly


# Ask user for the amount of days to base the prediction on
timespan = int(input("Enter the amount of days to take into account (e.g., For the last month: 30): "))

# Ask user for tickers
tickers_input = input("Enter stock tickers separated by spaces (e.g., AAPL NVDA AMD): ")
ticker_list = tickers_input.upper().split()

# Ask user for the next number of days to predict
nextdays = int(input("Enter the number of next days you want to predict: "))

for ticker in ticker_list:
    print(f"\nProcessing {ticker}...")
    dates, prices = get_data(ticker)
    prediction_day = len(dates)
    pred_rbf, pred_lin, pred_poly = predict_prices(dates, prices, prediction_day, ticker)
    print(f"Fetched {len(dates)} trading days for {ticker}")
    for i in range(nextdays):
        print(f"Day +{i+1}: RBF={pred_rbf[i]:.2f}, Linear={pred_lin[i]:.2f}, Poly={pred_poly[i]:.2f}")

plt.show()
