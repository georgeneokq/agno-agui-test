from agno.agent import Agent

def get_session_state(agent: Agent):
    """
    Retrieves agent session state.

    Returns:
        dict: Session State
    """
    return agent.workflow_session_state
