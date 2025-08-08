import os
from agno.agent import Agent
from agno.models.google import Gemini

stock_summary_agent = Agent(
    agent_id="stock_summary_agent",
    name="Stock Summary Agent",
    model=Gemini(
        id="gemini-2.5-flash",
        api_key=os.getenv("GEMINI_API_KEY")
    ),
    instructions="You are an Stock Summary agent. Based on previous agents' outputs, summarize the key points.",
    markdown=True
)
