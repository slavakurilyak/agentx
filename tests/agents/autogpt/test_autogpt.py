# tests/agents/autogpt/test_autogpt.py

from unittest.mock import patch

import pytest
from langchain.agents import Tool
from langchain.tools.file_management.read import ReadFileTool
from langchain.tools.file_management.write import WriteFileTool
from langchain.utilities import SerpAPIWrapper

from agentx.agents.autogpt.autogpt_agent import AutoGPTAgent
from agentx.memory.faiss import FAISSRetriever


@pytest.fixture
def autogpt_agent():
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
    return agent


@pytest.fixture
def expected_result():
    return {
        "thoughts": {
            "text": "I can use simple math to solve the problem of 11 + seven. "
            "I will use the 'write_file' command to save the result to a file for "
            "future reference.",
            "reasoning": "I can use basic arithmetic to solve the problem of 11 + seven. "
            "I will use the 'write_file' command to save the result to a file for "
            "future reference.",
            "plan": "- Use basic arithmetic to solve the problem of 11 + seven\n"
            "- Use the 'write_file' command to save the result to a file for future reference",
            "criticism": "I need to make sure I am using the most efficient command for "
            "the task at hand.",
            "speak": "I will solve the problem of 11 + seven using basic arithmetic "
            "and save the result to a file using the 'write_file' command.",
        },
        "command": {
            "name": "write_file",
            "args": {
                "file_path": "math_result.txt",
                "text": "The result of 11 + seven is 18.",
            },
        },
    }


def test_autogpt_agent(autogpt_agent):
    assert isinstance(autogpt_agent, AutoGPTAgent)


def test_autogpt_agent_solve_math_problem_and_save_result_to_file(
    autogpt_agent, expected_result
):
    with patch.object(autogpt_agent, "run", return_value=expected_result):
        result = autogpt_agent.run(["Help me do math: 11 + seven"])

    assert result["command"]["args"]["text"] == "The result of 11 + seven is 18."


def test_autogpt_agent_write_math_result_to_file(autogpt_agent, expected_result):
    with patch.object(autogpt_agent, "run", return_value=expected_result):
        result = autogpt_agent.run(["Help me do math: 11 + seven"])

    assert result["command"]["name"] == "write_file"
    assert result["command"]["args"]["file_path"] == "math_result.txt"
