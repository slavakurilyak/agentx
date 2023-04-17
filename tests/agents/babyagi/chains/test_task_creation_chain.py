import pytest
from langchain import PromptTemplate
from langchain.llms import BaseLLM

from agentx.agents.babyagi.chains import TaskCreationChain


class TestTaskCreationChain:
    @pytest.fixture
    def creation_chain(self, openai_llm):
        return TaskCreationChain.from_llm(openai_llm)

    def test_from_llm(self, creation_chain):
        assert isinstance(creation_chain, TaskCreationChain)
        assert isinstance(creation_chain.llm, BaseLLM)
        assert isinstance(creation_chain.prompt, PromptTemplate)

    def test_task_creation(self, creation_chain):
        """Test the task creation functionality by executing a task with a
        given objective, result, task description, and incomplete tasks.
        Verify that the output is a string with an upticking number at the
        beginning of each line.
        """
        objective = "Improve customer support"
        result = "Automated ticket categorization"
        task_description = (
            "Categorize support tickets using natural language processing"
        )
        incomplete_tasks = "1. Implement sentiment analysis," " 2. Develop chatbot"

        new_tasks_str = creation_chain.run(
            objective=objective,
            result=result,
            task_description=task_description,
            incomplete_tasks=incomplete_tasks,
        )

        new_tasks = new_tasks_str.strip().splitlines()
        assert len(new_tasks) > 0
        for idx, task in enumerate(new_tasks, start=1):
            task_num, task_text = task.split(".", 1)
            assert int(task_num.strip()) == idx
            assert task_text.strip()

        assert len(new_tasks) > 0
        assert all(isinstance(task, str) for task in new_tasks)
