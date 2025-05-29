import os
import argparse
import yaml
from pathlib import Path
from dotenv import load_dotenv

import yfinance as yf
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.tools import tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_anthropic import ChatAnthropic


@tool
def get_stock_data(symbol="AAPL"):
    """Get the current stock price for a given symbol."""
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="1mo", interval="1h")
    return hist


@tool
def buy_stock(symbol):
    """Places a Buy Order on the stock with the given symbol."""
    return f"Placing a buy on {symbol}"


@tool
def sell_stock(symbol):
    """Places a sell on the stock with the given symbol."""
    return f"Placing a sell on {symbol}"


@tool
def hold_stock(symbol):
    """Holds the stock with the given symbol."""
    return f"Holding {symbol}"


def load_config(config_path):
    """Load configuration from YAML file."""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


def main(config_path):
    """Main function to execute the trading agent."""
    # Load configuration
    config = load_config(config_path)
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
    
    #Initialize the LLM using config
    llm = ChatAnthropic(
        model=config["agent"]["name"], 
        api_key=api_key,
    )
    
    # Define the prompt template
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=config["agent"]["system_promt"]),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    # Define available tools
    tools = [get_stock_data, buy_stock, sell_stock, hold_stock]
    
    # Create the agent and executor
    agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    # Execute the trading decision
    response = agent_executor.invoke({
        "input": "Use the current stock data to determine if I should Buy the CRWV stock. Then using the decision, place a buy on CRWV",
        "chat_history": []
    })
    

    return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trading agent with configurable settings")
    parser.add_argument("config", help="Path to the configuration YAML file")
    
    args = parser.parse_args()
    main(args.config)
