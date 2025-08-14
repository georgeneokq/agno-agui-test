# agents/src/coding_agent.py
from pathlib import Path
from agno.agent import Agent
from agno.knowledge import KnowledgeBase
from agno.document.reader import RemoteDocumentReader
from agno.tools.file import FileTools
from agno.tools.apify import ApifyTools # For web scraping

# 1. Set up the Knowledge Base
knowledge_base = KnowledgeBase(
    name="Agno Docs Knowledge Base",
    document_reader=RemoteDocumentReader(url="https://docs.agno.com/introduction")  # Correct URL
)
knowledge_base.load(recreate=True) # Load the knowledge base.  recreate=True will force a refresh.

# 2.  Set up the File Tools:

file_tools = FileTools(Path("./output")) # Code will be output to ./output

# 3. Define the Agent:

coding_agent = Agent(
    name="Agno Coding Agent",
    knowledge=knowledge_base,
    search_knowledge=True, # Give the agent access to search the knowledge base.
    tools=[file_tools], # Added file tools so it can write to the FS
    instructions=[
        "You are an AI coding assistant.",
        "Use your knowledge base to understand the user's requirements.",
        "Output the code to a file.",
    ],
    show_tool_calls=True # Shows tool calls for debugging.
)

# Example usage (not part of the agent definition, but shows how to use it)
# To run this, you'd typically have another script that imports this agent.
if __name__ == "__main__":
    # Create the output directory if it doesn't exist.
    Path("./output").mkdir(parents=True, exist_ok=True)

    response = coding_agent.run("Write a python script that prints 'Hello, Agno!' to a file named hello.py")
    print(response)
