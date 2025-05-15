import yfinance as yf
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


def get_stock_data(symbol="AAPL"):
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="1d", interval="5m")
    return hist



llm = OllamaLLM(model="deepseek-r1:1.5b")

template = "Given the following stock data and news, should I buy, sell, or hold {symbol}? Data: {data}"
prompt = PromptTemplate(input_variables=["symbol", "data"], template=template)

chain = LLMChain(llm=llm, prompt=prompt)


def execute_trade(symbol):
    stock_data = get_stock_data(symbol)
  
    data_str = str(stock_data)  # Latest data   
    print(data_str)
    decision = chain.run(symbol=symbol, data=data_str)

    print(decision)


execute_trade("NVDA")