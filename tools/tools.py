# tools.py
import yfinance as yf

def get_stock_data_tool(inputs):
    symbol = inputs.get("symbol", "AAPL")
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="1mo", interval="1h")
    return hist.tail(5).to_json()

def buy_stock_tool(inputs):
    symbol = inputs["symbol"]
    return f"Placing a buy on {symbol}"

def sell_stock_tool(inputs):
    symbol = inputs["symbol"]
    return f"Placing a sell on {symbol}"

def hold_stock_tool(inputs):
    symbol = inputs["symbol"]
    return f"Holding {symbol}"

anthropic_tools = [
    {
        "name": "get_stock_data",
        "description": "Get the current stock price history for a given symbol.",
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "The stock symbol to look up (e.g., AAPL, TSLA)."
                }
            },
            "required": ["symbol"]
        }
    },
    {
        "name": "buy_stock",
        "description": "Place a buy order on a given stock symbol.",
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "The stock symbol to buy."
                }
            },
            "required": ["symbol"]
        }
    },
    {
        "name": "sell_stock",
        "description": "Place a sell order on a given stock symbol.",
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "The stock symbol to sell."
                }
            },
            "required": ["symbol"]
        }
    },
    {
        "name": "hold_stock",
        "description": "Hold the given stock symbol (no action).",
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "The stock symbol to hold."
                }
            },
            "required": ["symbol"]
        }
    }
]


tool_map = {
    "get_stock_data": get_stock_data_tool,
    # "buy_stock": buy_stock_tool,
    # "sell_stock": sell_stock_tool,
    # "hold_stock": hold_stock_tool,
}