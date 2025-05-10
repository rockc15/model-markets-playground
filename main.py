from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BASE_URL = os.getenv("https://paper-api.alpaca.markets/v2")

trading_client = TradingClient(API_KEY, API_SECRET, paper=True)

# Define the market order parameters
market_order_data = MarketOrderRequest(
    symbol="NVDA",          # Stock symbol
    qty=1,                 # Number of shares
    side=OrderSide.BUY,     # Buy or Sell
    time_in_force=TimeInForce.GTC  # Good Till Cancelled
)

# Submit the market order
try:
    market_order = trading_client.submit_order(order_data=market_order_data)
    print(f"Market order placed: {market_order.id} for {market_order.qty} shares of {market_order.symbol}")
except Exception as e:
    print(f"Error placing order: {e}")