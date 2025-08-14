import os
from agno.workflow.v2 import Step, Workflow, StepInput, StepOutput
from agents.stock_price_agent import stock_price_agent
from agents.company_news_agent import company_news_agent
from agents.stock_summary_agent import stock_summary_agent
from agno.agent import Agent
from agno.team import Team
from agno.models.google import Gemini

def set_state(agent: Agent, stock_symbol: str, company_name: str):
    """
    Extract stock symbol and company name from user input.
    """
    if not agent.workflow_session_state:
        agent.workflow_session_state = {}

    agent.workflow_session_state["stock_symbol"] = stock_symbol
    agent.workflow_session_state["company_name"] = company_name

get_stock_price_step = Step(
    name="get_stock_price",
    description="Get the stock price for a specified company",
    agent=stock_price_agent,
)
get_company_news_step = Step(
    name="get_company_news",
    description="Get news on a specified company",
    agent=company_news_agent,
)

planner_agent = Agent(
    model=Gemini(
        id="gemini-2.5-flash",
        api_key=os.getenv("GEMINI_API_KEY")
    ),
    instructions=[
        "Given a company name, retrieve its matching stock symbol or vice-versa, and set both into workflow session state."
        "Example: Tesla <-> TSLA"
        "Do not output anything, just set state."
    ],
    tools=[set_state],
    add_name_to_instructions=True,
    add_state_in_messages=True
)

team = Team(
    model=Gemini(
        id="gemini-2.5-flash",
        api_key=os.getenv("GEMINI_API_KEY")
    ),
    mode="collaborate",
    members=[stock_price_agent, company_news_agent],
    stream=True,
    add_state_in_messages=True
)

planner_agent_step = Step(
    name="planner_agent_step",
    description="Extracts information from user input and sets it into workflow session state",
    agent=planner_agent,
)

def debug_session_state(step_input: StepInput):
    print("-------------------------")
    print("Session State")
    print("-------------------------")
    print(team.workflow_session_state)
    # Echo
    return StepOutput(content=step_input.previous_step_content)

# TODO: Find out whether we could improve this flow, redundant input/output to and from the team members.
#       Perhaps collaborate mode is the not the play here.
collaboration_step = Step(
    name="collaboration_step",
    description="Process workflow session state for final output",
    team=team
)

stock_research_workflow = Workflow(
    name="Stock research workflow",
    steps=[
        planner_agent_step,
        debug_session_state,
        collaboration_step,
    ],
    stream=True,
    stream_intermediate_steps=True,
    workflow_session_state={"stock_symbol": "", "company_name": ""},
)
