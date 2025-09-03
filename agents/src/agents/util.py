from agno.agent import Agent
from agno.team import Team
from typing import Optional

def get_session_state(agent: Agent, state_key: str):
    """Retrieve a key from session state."""
    if agent.team_session_state:
        return agent.team_session_state.get(state_key)


def set_session_state(agent: Team, stock_symbol: Optional[str] = None, company_name: Optional[str] = None, summary: Optional[str] = None):
    """Update the team's session state. Set parameter to None to retain original value. You may set multiple at once to save function calls."""
    if not agent.team_session_state:
        agent.team_session_state = {}
    
    if stock_symbol:
        agent.team_session_state["stock_symbol"] = stock_symbol
    if company_name:
        agent.team_session_state["company_name"] = company_name
    if summary:
        agent.team_session_state["summary"] = summary
