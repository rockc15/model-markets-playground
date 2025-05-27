import yfinance as yf
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.tools import tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_anthropic import ChatAnthropic
import os
from pathlib import Path
from dotenv import load_dotenv


@tool
def get_stock_data(symbol="AAPL"):
    """Get the current stock price for a given symbol."""
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="1mo", interval="1h")
    return hist

@tool
def buy_stock(symbol):
    """Places a Buy Order on the stock with the given symbol."""
    return f"Placing a buy on{symbol}"

@tool
def sell_stock(symbol):
    """Places a sell on the stock with the given symbol."""
    return f"Placing a sell on{symbol}"

@tool
def hold_stock(symbol):
    """Holds the stock with the given symbol."""
    return f"Holding {symbol}"

# Path to the .env file in another directory
env_path = Path(__file__).resolve().parent / 'config' / '.env'
load_dotenv(dotenv_path=env_path)


api_key = os.getenv("ANTHROPIC_API_KEY")

print(api_key)


llm = ChatAnthropic(
    model="claude-opus-4-20250514",  # or claude-3-sonnet-20240229 / claude-3-haiku-20240307
    api_key=api_key,
)



prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="You are a financial analysis agent with access to tools that can retrieve up-to-date stock data. Your task is to analyze the current market data and help perform trading task"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

tools = [get_stock_data, buy_stock, sell_stock,hold_stock]

# # Define LLM
# llm = ChatOllama(model="qwen3:8b")

agent = create_tool_calling_agent(llm=llm , tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

response = agent_executor.invoke({
    "input": "Use the current stock data to detemine if I should Buy the CRWV stock. Then using the decesion, place a buy on CRWV",
    "chat_history": []
})

# # response = agent_executor.invoke({
# #     "input": "Use the current stock data to determine whether I should Buy, Hold, or Sell one of the following stocks AAPL (Apple) MSFT (Microsoft) NVDA (NVIDIA) AMZN (Amazon) META (Meta Platforms). Based on your analysis, choose the single best stock and make a recommendation. Then, execute the appropriate action—buy, sell, or hold—for the selected stock.",
# #     "chat_history": []
# # })

# print(response)

# # Define prompt
# # template = "Given the following stock data and news, should I buy, sell, or hold {symbol}? Data: {data}"
# # prompt = PromptTemplate(input_variables=["symbol", "data"], template=template)

# # Build chain using new RunnableSequence syntax
# # chain = prompt | llm

# def execute_trade(symbol):
#     stock_data = get_stock_data(symbol)
#     data_str = str(stock_data)  # Use only last 5 rows for brevity
#     print(data_str)

#     # Use invoke instead of run
#     decision = chain.invoke({"symbol": symbol, "data": data_str})

#     print(decision.content)


# execute_trade("NVDA")
