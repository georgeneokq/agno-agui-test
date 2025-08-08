import os
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.yfinance import YFinanceTools

stock_price_agent = Agent(
    agent_id="stock_price_agent",
    name="Stock Price Agent",
    model=Gemini(
        id="gemini-2.5-flash",
        api_key=os.getenv("GEMINI_API_KEY")
    ),
    tools=[YFinanceTools()],
    instructions="You are a stock price agent. Return data of specifed stock.",
)
