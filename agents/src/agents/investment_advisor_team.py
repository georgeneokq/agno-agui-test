import os
from agno.team import Team
from agno.models.google import Gemini
from agno.storage.sqlite import SqliteStorage
from agents.stock_price_agent import stock_price_agent
from agents.company_news_agent import company_news_agent
from agents.stock_summary_agent import stock_summary_agent

def update_latest_stock_price(team: Team, company_name: str, stock_price: float):
    """
    Caches the latest stock price
    """
    assert team.session_state
    print("Before update")
    print(team.session_state)
    
    # Standardize to lower case
    key = company_name.lower()

    team.session_state['latest_stock_price'][key] = stock_price
    print("After update")
    print(team.session_state)

# For testing collaborate mode, remove the stock summary agent and the instruction referencing it.
# For testing coordinate mode, include the stock summary agent and the instruction referencing it.
investment_advisor_team = Team(
    team_id="investment_advisor_team",
    name="Investment Advisor Team",
    model=Gemini(
        id="gemini-2.5-flash",
        api_key=os.getenv("GEMINI_API_KEY")
    ),
    members=[
        stock_price_agent,
        company_news_agent,
        stock_summary_agent
    ],
    instructions=[
        "You should expect a company or a stock symbol as an input."
        "Firstly, attempt to get the stock price from your state, if not cached in state then get it from Stock Price Agent."
        "State in your response if the stock price was retrieved from cache or not."
        "Then get related news from Company News Agent."
        "Call `update_latest_stock_price` for caching."
        "Finally, ask the Stock Summary Agent to summarize the price and news."
        # "Finally, summarize the price and news."
        # "Respond to user's query, redirect to suitable member of the team."
    ],
    tools=[
        update_latest_stock_price
    ],
    mode="coordinate",
    stream=True,
    stream_intermediate_steps=True,
    add_datetime_to_instructions=True,
    enable_agentic_context=True,
    enable_team_history=True,
    share_member_interactions=True,
    add_state_in_messages=True,
    storage=SqliteStorage(table_name="agent_sessions", db_file="/tmp/data.db"),
    markdown=True,
    session_state={
      "latest_stock_price": {}
    }
)
