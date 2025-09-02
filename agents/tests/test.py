import os
import pytest
import scenario
from agno.agent import Agent
from agno.models.google import Gemini

# Configure Scenario defaults (model for user simulator and judge)
scenario.configure(default_model="openai/gpt-4.1-mini")

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_vegetarian_recipe_agent() -> None:
    # 1. Define an AgentAdapter to wrap your agent
    class VegetarianRecipeAgentAdapter(scenario.AgentAdapter):
        agent: Agent

        def __init__(self) -> None:
            self.agent = Agent(
                model=Gemini(
                  id="gemini-2.5-flash",
                  api_key=os.getenv("GEMINI_API_KEY")
                ),
                markdown=True,
                debug_mode=True,
                instructions="You are a vegetarian recipe agent.",
            )

        async def call(self, input: scenario.AgentInput) -> scenario.AgentReturnTypes:
            response = self.agent.run(
                message=input.last_new_user_message_str(), # Pass only the last user message
                session_id=input.thread_id, # Pass the thread id, this allows the agent to track history
            )
            return response.content

    # 2. Run the scenario simulation
    result = await scenario.run(
        name="dinner recipe request",
        description="User is looking for a vegetarian dinner idea.",
        agents=[
            VegetarianRecipeAgentAdapter(),
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(
                criteria=[
                    "Agent should not ask more than two follow-up questions",
                    "Agent should generate a recipe",
                    "Recipe should include a list of ingredients",
                    "Recipe should include step-by-step cooking instructions",
                    "Recipe should be vegetarian and not include any sort of meat",
                ]
            ),
        ],
    )

    # 3. Assert and inspect the result
    assert result.success