import yfinance as yf
import matplotlib.pyplot as plt

# Get historical data for Apple (AAPL)
aapl = yf.Ticker("AAPL")
hist = aapl.history(period="1mo")  # Get data for the past month

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(hist.index, hist['Close'], label='AAPL Closing Price', color='blue')
plt.title('Apple (AAPL) Stock Closing Prices - Last 1 Year')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.grid(True)
plt.legend()

plt.show()