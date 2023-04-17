from unittest.mock import MagicMock

import pytest
from agentx.agents.babyagi.chains import TaskCreationChain, TaskPrioritizationChain
from agentx.agents.babyagi.utils import (
    _get_top_tasks,
    execute_task,
    get_next_task,
    prioritize_tasks,
)


class TestGetTopTasks:
    def test_get_top_tasks(self):
        # Create a mock vectorstore with sample tasks
        mock_vectorstore = MagicMock()
        mock_vectorstore.similarity_search_with_score.return_value = [
            (MagicMock(metadata={"task": "Task 1"}), 0.8),
            (MagicMock(metadata={"task": "Task 2"}), 0.7),
            (MagicMock(metadata={"task": "Task 3"}), 0.6),
        ]

        query = "Sample query"
        k = 3

        top_tasks = _get_top_tasks(
            vectorstore=mock_vectorstore,
            query=query,
            k=k,
        )

        assert isinstance(top_tasks, list)
        assert len(top_tasks) == k
        assert top_tasks == ["Task 1", "Task 2", "Task 3"]

        # Test with empty results
        mock_vectorstore.similarity_search_with_score.return_value = []
        top_tasks = _get_top_tasks(
            vectorstore=mock_vectorstore,
            query=query,
            k=k,
        )
        assert top_tasks == []


class TestExecuteTask:
    def test_execute_task(self):
        # Create a mock vectorstore
        mock_vectorstore = MagicMock()
        mock_vectorstore.similarity_search_with_score.return_value = [
            (MagicMock(metadata={"task": "Task 1"}), 0.8),
            (MagicMock(metadata={"task": "Task 2"}), 0.7),
        ]

        # Create a mock execution_chain
        mock_execution_chain = MagicMock()
        mock_execution_chain.run.return_value = "Executed task result"

        objective = "Sample objective"
        task = "Sample task"
        k = 2

        executed_task_result = execute_task(
            vectorstore=mock_vectorstore,
            execution_chain=mock_execution_chain,
            objective=objective,
            task=task,
            k=k,
        )

        assert isinstance(executed_task_result, str)
        assert executed_task_result == "Executed task result"

        # Test with k = 0 (empty context)
        k = 0
        executed_task_result = execute_task(
            vectorstore=mock_vectorstore,
            execution_chain=mock_execution_chain,
            objective=objective,
            task=task,
            k=k,
        )
        assert executed_task_result == "Executed task result"


class TestGetNextTask:
    @pytest.fixture
    def task_creation_chain(self, openai_llm):
        return TaskCreationChain.from_llm(openai_llm)

    def test_get_next_task(self, task_creation_chain):
        """Test the get_next_task function to ensure it returns a list of new
        tasks.

        Args:
            task_creation_chain (TaskCreationChain): An instance of the
                                                     TaskCreationChain class.

        This test checks if the function returns a list of dictionaries with a
        "task_name" key.
        """

        result = "The last task was completed successfully."
        task_description = "The last task was to analyze customer feedback."
        task_list = [
            "Improve customer support response time",
            "Update knowledge base articles",
        ]
        objective = "Enhance customer satisfaction"

        new_tasks = get_next_task(
            task_creation_chain=task_creation_chain,
            result=result,
            task_description=task_description,
            task_list=task_list,
            objective=objective,
        )

        assert isinstance(new_tasks, list)
        assert all(isinstance(task, dict) for task in new_tasks)
        assert all("task_name" in task for task in new_tasks)


class TestPrioritizeTasks:
    """Test class for the prioritize_tasks function."""

    @pytest.fixture
    def task_prioritization_chain(self, openai_llm):
        return TaskPrioritizationChain.from_llm(openai_llm)

    def test_prioritize_tasks(self, task_prioritization_chain):
        """Test the prioritize_tasks function to ensure it returns a list
           of prioritized tasks.

        Args:
            task_prioritization_chain (TaskPrioritizationChain):
                            An instance of the TaskPrioritizationChain class.

        This test checks if the function returns a list of dictionaries with
        a "task_id" and "task_name" key.
        """
        this_task_id = 1
        task_list = [
            {"task_name": "Improve customer support response time"},
            {"task_name": "Update knowledge base articles"},
        ]
        objective = "Enhance customer satisfaction"

        prioritized_tasks = prioritize_tasks(
            task_prioritization_chain=task_prioritization_chain,
            this_task_id=this_task_id,
            task_list=task_list,
            objective=objective,
        )

        assert isinstance(prioritized_tasks, list)
        assert all(isinstance(task, dict) for task in prioritized_tasks)
        assert all(
            "task_id" in task and "task_name" in task for task in prioritized_tasks
        )
        assert len(prioritized_tasks) == len(task_list)
