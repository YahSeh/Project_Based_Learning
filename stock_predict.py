import csv
import numpy as np
from sklearn.svm import SVR
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime, timedelta
import warnings
from sklearn.exceptions import DataConversionWarning

warnings.simplefilter("ignore", category=FutureWarning)
warnings.simplefilter("ignore", category=DataConversionWarning)

'''def get_data(filename):
    with open(filename, 'r') as csvfile:
        csvFileReader = csv.reader(csvfile)
        next(csvFileReader)
        for row in csvFileReader:
            dates.append(int(row[0].split('-')[0]))
            prices.append(float(row[2]))
    return
'''

def get_data(ticker):
    end = datetime.now()
    start = end - timedelta(days=183)
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
    x_input = np.array([[x]])
    pred_rbf = svr_rbf.predict(x_input)[0]
    pred_lin = svr_lin.predict(x_input)[0]
    pred_poly = svr_poly.predict(x_input)[0]

    # Resize Figures
    plt.figure(figsize=(len(dates) * 0.5, 6))

    # Plot actual data and models
    plt.scatter(dates, prices, color='black', label='Actual Data')
    # RBF Prediction
    plt.plot(dates, svr_rbf.predict(dates), color='red', label='RBF model')
    plt.text(x + 2, pred_rbf, f"{pred_rbf:.2f}", color='red')
    # Linear Prediction
    plt.plot(dates, svr_lin.predict(dates), color='green', label='Linear model')
    plt.text(x + 2, pred_lin, f"{pred_lin:.2f}", color='green')
    # Polynomial Prediction
    plt.plot(dates, svr_poly.predict(dates), color='blue', label='Polynomial model')
    plt.text(x + 2, pred_poly, f"{pred_poly:.2f}", color='blue')
    
    # Plot predictions
    plt.scatter(x, pred_rbf, color='red', marker='x', s=100, label='RBF Prediction')
    plt.scatter(x, pred_lin, color='green', marker='x', s=100, label='Linear Prediction')
    plt.scatter(x, pred_poly, color='blue', marker='x', s=100, label='Polynomial Prediction')


    plt.xlabel('Day Index')
    plt.ylabel('Price')
    plt.title(f'{ticker} Stock Price Prediction (Last {len(dates)} Days)')
    plt.legend()
    plt.tight_layout
    plt.show(block=False)

    return pred_rbf, pred_lin, pred_poly

# Ask user for tickers
tickers_input = input("Enter stock tickers separated by spaces (e.g., AAPL NVDA AMD): ")
ticker_list = tickers_input.upper().split()

for ticker in ticker_list:
    print(f"\nProcessing {ticker}...")
    dates, prices = get_data(ticker)
    prediction_day = len(dates)
    predicted_price = predict_prices(dates, prices, prediction_day, ticker)
    print(f"{ticker} predicted prices for next day:\nRBF: {predicted_price[0]:.2f}, Linear: {predicted_price[1]:.2f}, Poly: {predicted_price[2]:.2f}")

plt.show()


'''ticker = "NVDA"
dates, prices = get_data(ticker)
prediction_day = len(dates)
predicted_price = predict_prices(dates, prices, prediction_day

print(f"Predicted prices for next day:\nRBF: {predicted_price[0]:.2f}, Linear: {predicted_price[1]:.2f}, Poly: {predicted_price[2]:.2f}")'''

