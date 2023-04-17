"""Test cases related to agentx/baby_agi_controller.py"""
import pytest
from agentx.baby_agi_controller import BabyAGI, Task


def test_task_creation():
    description = "Initial Task"
    priority = 1

    task = Task(description=description, priority=priority)
    assert task.priority == priority
    assert task.description == description


class TestBabyAgi:
    @pytest.fixture(autouse=True)
    def set_up(self):
        self.baby_agi = BabyAGI(objective="Solve world hunger.")

    def test_baby_agi_properties(self):
        assert self.baby_agi.objective == "Solve world hunger."
        assert self.baby_agi.task_list == []

    def test_add_task(self):
        description = "Initial Task"
        priority = 1
        task = Task(description=description, priority=priority)
        self.baby_agi.add_task(task)
        assert len(self.baby_agi.task_list) == 1
        assert task == self.baby_agi.task_list[0]
