from alpaca.trading.client import TradingClient
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BASE_URL = os.getenv("https://paper-api.alpaca.markets/v2")

trading_client = TradingClient(API_KEY, API_SECRET)
account = trading_client.get_account()

class TradingAccount:
    def __init__(self):
        trading_client = TradingClient(API_KEY, API_SECRET, paper=True)
        self.account = trading_client.get_account()

    def getTodaysBalanceChange(self):
        return float(self.account.equity) - float(self.account.last_equity)


if __name__=="__main__":
    testAccount = TradingAccount()

    print(testAccount.getTodaysBalanceChange())