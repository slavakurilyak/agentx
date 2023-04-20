# tests/agents/babyagi/chains/test_task_execution_chain.py

import pytest
from langchain import PromptTemplate
from langchain.llms import BaseLLM

from agentx.agents.babyagi.chains import TaskExecutionChain


class TestTaskExecutionChain:
    @pytest.fixture
    def execution_chain(self, openai_llm):
        return TaskExecutionChain.from_llm(openai_llm)

    def test_from_llm(self, execution_chain):
        assert isinstance(execution_chain, TaskExecutionChain)
        assert isinstance(execution_chain.llm, BaseLLM)
        assert isinstance(execution_chain.prompt, PromptTemplate)

    def test_task_execution(self, execution_chain):
        objective = "Sort a list of numbers"
        context = "Previous task: find the largest number in a list"
        task = "Sort the list [5, 3, 1, 4, 2]"

        response = execution_chain.run(objective=objective, context=context, task=task)

        assert isinstance(response, str)
        assert "1, 2, 3, 4, 5" in response or "1 2 3 4 5" in response
