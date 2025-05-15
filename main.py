import yfinance as yf
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence


def get_stock_data(symbol="AAPL"):
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="1d", interval="5m")
    return hist


# Define LLM
llm = OllamaLLM(model="deepseek-r1:1.5b")

# Define prompt
template = "Given the following stock data and news, should I buy, sell, or hold {symbol}? Data: {data}"
prompt = PromptTemplate(input_variables=["symbol", "data"], template=template)

# Build chain using new RunnableSequence syntax
chain = prompt | llm

def execute_trade(symbol):
    stock_data = get_stock_data(symbol)
    data_str = str(stock_data)  # Use only last 5 rows for brevity
    print(data_str)

    # Use invoke instead of run
    decision = chain.invoke({"symbol": symbol, "data": data_str})

    print(decision)


execute_trade("NVDA")
