# agentx/agents/autogpt/main.py

from langchain.agents import Tool
from langchain.tools.file_management.read import ReadFileTool
from langchain.tools.file_management.write import WriteFileTool
from langchain.utilities import SerpAPIWrapper

from agentx.agents.autogpt.autogpt_agent import AutoGPTAgent
from agentx.memory.faiss import FAISSRetriever


def run_autogpt():
    suggested_objective = "Help me do math: 11 + seven"
    user_objective = input(
        f"What is your objective? (Press enter to use the suggested objective: "
        f"'{suggested_objective}') "
    )

    if not user_objective:
        objective = suggested_objective
    else:
        objective = user_objective

    search = SerpAPIWrapper()
    tools = [
        Tool(
            name="search",
            func=search.run,
            description="useful for when you need to answer questions about current events. "
            "You should ask targeted questions",
        ),
        WriteFileTool(),
        ReadFileTool(),
    ]

    memory = FAISSRetriever()

    agent = AutoGPTAgent(tools=tools, memory=memory)
    agent.agent.chain.verbose = True
    agent.run([objective])


if __name__ == "__main__":
    run_autogpt()
