import yfinance as yf
import matplotlib.pyplot as plt



class YahooFinance:
    def __init__(self):
        pass

    def getHistoricalStockData(self,symbol,period="6mo",interval="1hr"):
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period, interval=interval) # Get data for the past month
        return hist
    
    def plotHistoricalStockData(self,hist):
        # Create the plot
        plt.figure(figsize=(10, 6))
        plt.plot(hist.index, hist['Close'], label='AAPL Closing Price', color='blue')
        plt.title('Apple (AAPL) Stock Closing Prices - Last 1 Year')
        plt.xlabel('Date')
        plt.ylabel('Price (USD)')
        plt.grid(True)
        plt.legend()

        plt.show()


