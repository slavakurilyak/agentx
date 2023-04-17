import pytest
from langchain import PromptTemplate
from langchain.llms import BaseLLM

from agentx.agents.babyagi.chains import TaskPrioritizationChain


class TestTaskPrioritizationChain:
    @pytest.fixture
    def prioritization_chain(self, openai_llm):
        return TaskPrioritizationChain.from_llm(openai_llm)

    def test_from_llm(self, prioritization_chain):
        assert isinstance(prioritization_chain, TaskPrioritizationChain)
        assert isinstance(prioritization_chain.llm, BaseLLM)
        assert isinstance(prioritization_chain.prompt, PromptTemplate)

    def test_task_prioritization(self, prioritization_chain):
        """Test the task prioritization functionality of
        TaskPrioritizationChain.

        This test provides a list of tasks, a next task ID,
        and an objective to the TaskPrioritizationChain. It
        then checks that the returned string contains the
        expected prioritized tasks.
        """
        task_names = """
        [Solve the efficiency issues,
        Reason about potential efficiency issues]
        """

        next_task_id = 3
        objective = "Improve overall team efficiency"

        prioritized_tasks_str = prioritization_chain.run(
            task_names=task_names,
            next_task_id=next_task_id,
            objective=objective,
        )

        assert prioritized_tasks_str.strip().split("\n") == [
            "3. Reason about potential efficiency issues",
            "4. Solve the efficiency issues",
        ]
