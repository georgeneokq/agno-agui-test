import os
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.yfinance import YFinanceTools

from agents.util import get_session_state

stock_price_agent = Agent(
    agent_id="stock_price_agent",
    name="Stock Price Agent",
    model=Gemini(
        id="gemini-2.5-flash",
        api_key=os.getenv("GEMINI_API_KEY")
    ),
    tools=[
      YFinanceTools(),
      get_session_state
    ],
    instructions=[
      "You are a stock price agent."
      "1. Call `get_session_state` to retrieve `stock_symbol`"
      "2. Retrieve price data of `stock_symbol`."
    ],
    markdown=True
)
