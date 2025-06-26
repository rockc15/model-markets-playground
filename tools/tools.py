# tools.py
import yfinance as yf
import json
from datetime import datetime

def get_stock_data_tool(inputs):
    """Get comprehensive stock data including price history and key metrics."""
    symbol = inputs.get("symbol", "AAPL")
    period = inputs.get("period", "1mo")
    
    try:
        ticker = yf.Ticker(symbol)
        
        # Get historical data
        hist = ticker.history(period=period)
        
        # Get stock info
        info = ticker.info
        
        # Prepare comprehensive data
        stock_data = {
            "symbol": symbol,
            "current_price": float(hist['Close'].iloc[-1]) if not hist.empty else None,
            "price_change": float(hist['Close'].iloc[-1] - hist['Close'].iloc[-2]) if len(hist) > 1 else 0,
            "price_change_percent": float((hist['Close'].iloc[-1] - hist['Close'].iloc[-2]) / hist['Close'].iloc[-2] * 100) if len(hist) > 1 else 0,
            "volume": int(hist['Volume'].iloc[-1]) if not hist.empty else None,
            "company_name": info.get('longName', symbol),
            "sector": info.get('sector'),
            "market_cap": info.get('marketCap'),
            "pe_ratio": info.get('trailingPE'),
            "52_week_high": info.get('fiftyTwoWeekHigh'),
            "52_week_low": info.get('fiftyTwoWeekLow'),
            "recent_prices": {str(date): float(price) for date, price in hist['Close'].tail(5).items()}
        }
        
        return json.dumps(stock_data, indent=2, default=str)
        
    except Exception as e:
        return f"Error retrieving stock data for {symbol}: {str(e)}"

def get_market_overview_tool(inputs):
    """Get overview of major market indices for market context."""
    indices = {
        "^GSPC": "S&P 500",
        "^DJI": "Dow Jones",
        "^IXIC": "NASDAQ"
    }
    
    market_data = {}
    
    try:
        for symbol, name in indices.items():
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="5d")
            if not hist.empty:
                current = float(hist['Close'].iloc[-1])
                previous = float(hist['Close'].iloc[-2]) if len(hist) > 1 else current
                change = current - previous
                change_percent = (change / previous * 100) if previous != 0 else 0
                
                market_data[name] = {
                    "symbol": symbol,
                    "current": current,
                    "change": change,
                    "change_percent": round(change_percent, 2)
                }
        
        return json.dumps(market_data, indent=2)
        
    except Exception as e:
        return f"Error retrieving market overview: {str(e)}"

def buy_stock_tool(inputs):
    """Simulate placing a buy order (recommendation only)."""
    symbol = inputs["symbol"]
    quantity = inputs.get("quantity", 1)
    return f"RECOMMENDATION: BUY {quantity} shares of {symbol}"

def sell_stock_tool(inputs):
    """Simulate placing a sell order (recommendation only)."""
    symbol = inputs["symbol"]
    quantity = inputs.get("quantity", 1)
    return f"RECOMMENDATION: SELL {quantity} shares of {symbol}"

def hold_stock_tool(inputs):
    """Recommend holding the stock position."""
    symbol = inputs["symbol"]
    reason = inputs.get("reason", "Based on current analysis")
    return f"RECOMMENDATION: HOLD {symbol}. Reason: {reason}"

# Enhanced tool definitions for Anthropic with proper web search
anthropic_tools = [
    {
        "name": "get_stock_data",
        "description": "Get comprehensive stock data including current price, historical performance, volume, and key financial metrics for detailed analysis.",
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "The stock symbol to analyze (e.g., AAPL, TSLA, NVDA)."
                },
                "period": {
                    "type": "string",
                    "description": "Time period for historical data. Options: '1d', '5d', '1mo', '3mo', '6mo', '1y'. Default is '1mo'."
                }
            },
            "required": ["symbol"]
        }
    },
    {
        "name": "get_market_overview",
        "description": "Get current overview of major market indices (S&P 500, Dow Jones, NASDAQ) to understand overall market sentiment and conditions.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "web_search",
        "description": "Search the web for current information, news, and data to supplement analysis. Returns structured results with sources and citations.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to find relevant information on the web."
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of search results to return. Default is 5.",
                    "minimum": 1,
                    "maximum": 10
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "buy_stock",
        "description": "Generate a BUY recommendation for a stock after analysis.",
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "The stock symbol to recommend buying."
                },
                "quantity": {
                    "type": "integer",
                    "description": "Number of shares to recommend buying. Default is 1.",
                    "minimum": 1
                }
            },
            "required": ["symbol"]
        }
    },
    {
        "name": "sell_stock",
        "description": "Generate a SELL recommendation for a stock after analysis.",
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "The stock symbol to recommend selling."
                },
                "quantity": {
                    "type": "integer",
                    "description": "Number of shares to recommend selling. Default is 1.",
                    "minimum": 1
                }
            },
            "required": ["symbol"]
        }
    },
    {
        "name": "hold_stock",
        "description": "Generate a HOLD recommendation for a stock after analysis.",
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "The stock symbol to recommend holding."
                },
                "reason": {
                    "type": "string",
                    "description": "Reason for the hold recommendation."
                }
            },
            "required": ["symbol"]
        }
    }
]
