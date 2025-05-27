from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BASE_URL = os.getenv("https://paper-api.alpaca.markets/v2")


class AlpacaTrading():
    def __init__(self):
        self.trading_client = TradingClient(API_KEY, API_SECRET, paper=True)


    def listCurrentPositions(self):
        try:
            positions =self.trading_client.get_all_positions()
            # Display your holdings
            print(positions)
            for position in positions:
                print(f"Symbol: {position.symbol}")
                print(f"Quantity: {position.qty}")
                print(f"Market Value: ${position.market_value}")
                print(f"Average Entry Price: ${position.avg_entry_price}")
                print(f"Unrealized P/L: ${position.unrealized_pl}")
                print("-" * 30)
                return positions
        except Exception as e:
            print(f"Error Listing Positions: {e}")


    def submitMarkerOrder(self, symbol,qty=1,time_in_force=TimeInForce.DAY):
        try:
            market_order_data=  MarketOrderRequest(
                symbol=symbol,          # Stock symbol
                qty=qty,                 # Number of shares
                side=OrderSide.BUY,     # Buy or Sell
                time_in_force=time_in_force # Good Till Cancelled
            )
            market_order =self.trading_client.submit_order(order_data=market_order_data)
            print(f"Market order placed: {market_order.id} for {market_order.qty} shares of {market_order.symbol}")
        except Exception as e:
            print(f"Error placing order: {e}")


    def submitSellOrder(self, symbol,qty=1,time_in_force=TimeInForce.DAY):
        try:    
            sell_order_data = MarketOrderRequest(
                symbol=symbol,               # Replace with your desired stock symbol
                qty=qty,                       # Number of shares to sell
                side=OrderSide.SELL,         # Specify the order side as SELL
                time_in_force=time_in_force  # Order valid for the day
            )
            order =self.trading_client.submit_order(order_data=sell_order_data)
            print(f"Sell order placed: {sell_order_data.id} for {sell_order_data.qty} shares of {sell_order_data.symbol}")
        except Exception as e:
            print(f"Error Selling order: {e}")



trader = AlpacaTrading()
trader.listCurrentPositions()

trader.submitMarkerOrder("NVDA")
# trader.submitSellOrder("NVDA")

