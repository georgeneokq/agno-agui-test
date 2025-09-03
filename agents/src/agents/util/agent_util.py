from agno.agent import Agent
from agno.team import Team

def get_session_state(agent: Agent):
    """
    Retrieves agent session state.

    Returns:
        dict: Session State
    """
    # return agent.workflow_session_state
    return agent.team_session_state

def set_session_state(agent: Team, stock_symbol: str | None = None, company_name: str | None = None, summary: str | None = None):
    """
    Set session state. Pass in None to keep a state variable unchanged.
    """
    # if not agent.workflow_session_state:
    if not agent.team_session_state:
        # agent.workflow_session_state = {}
        agent.team_session_state = {}

    if stock_symbol:
        agent.team_session_state["stock_symbol"] = stock_symbol
    if company_name:
        agent.team_session_state["company_name"] = company_name
    if summary:
        agent.team_session_state["summary"] = summary
