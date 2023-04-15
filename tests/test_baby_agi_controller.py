import pytest
from agentx.baby_agi_controller import Task, BabyAGI, BabyAGIAgent, BabyAGIWithToolsAgent

class TestTask:
    def test_task_creation(self):
        description = 'Complete objective'
        priority = 1
        task = Task(description=description, priority=priority)
        assert task.priority == priority
        assert task.description == description

class TestBabyAGI:
    @pytest.fixture(autouse=True)
    def set_up(self):
        self.baby_agi = BabyAGI(objective='Solve world hunger.')

    def test_baby_agi_properties(self):
        assert self.baby_agi.objective == 'Solve world hunger.'
        assert self.baby_agi.task_list == []

    def test_add_task_based_on_user_objective(self):
        objective = "Solve world hunger."
        agent = self.baby_agi.get_agent(objective)
        agent.process_prompt()
        assert len(self.baby_agi.task_list) == 1
        assert self.baby_agi.task_list[0].description == objective

    def test_add_task(self):
        description = 'Complete objective'
        priority = 1
        task = Task(description=description, priority=priority)
        self.baby_agi.add_task(task)
        assert len(self.baby_agi.task_list) == 1
        assert self.baby_agi.task_list[0].description == description

    def test_prioritize_tasks(self):
        task1 = Task(description='Task 1', priority=1)
        task2 = Task(description='Task 2', priority=2)
        task3 = Task(description='Task 3', priority=3)
        self.baby_agi.add_task(task1)
        self.baby_agi.add_task(task2)
        self.baby_agi.add_task(task3)
        prioritized_tasks = self.baby_agi.prioritize_tasks()
        assert len(prioritized_tasks) == 3
        assert prioritized_tasks[0].description == 'Task 3'
        assert prioritized_tasks[1].description == 'Task 2'
        assert prioritized_tasks[2].description == 'Task 1'

    def test_execute_task(self):
        description = 'Complete objective'
        priority = 1
        task = Task(description=description, priority=priority)
        self.baby_agi.add_task(task)
        result = self.baby_agi.execute_task()
        assert result == description
        assert len(self.baby_agi.task_list) == 0

    def test_print_task_info(self, capsys):
        task1 = Task(description='Task 1', priority=1)
        task2 = Task(description='Task 2', priority=2)
        self.baby_agi.add_task(task1)
        self.baby_agi.add_task(task2)
        self.baby_agi.print_task_info()
        assert capsys.readouterr().out.strip() == '*****TASK LIST*****\nTask 1\nTask 2\n\n*****NEXT TASK*****\nTask 1'

    def test_print_task_list(self, capsys):
        task1 = Task(description='Task 1', priority=1)
        task2 = Task(description='Task 2', priority=2)
        self.baby_agi.add_task(task1)
        self.baby_agi.add_task(task2)
        self.baby_agi.print_task_list()
        assert capsys.readouterr().out.strip() == '*****TASK LIST*****\nTask 1\nTask 2'

    def test_print_next_task(self, capsys):
        task1 = Task(description='Task 1', priority=1)
        task2 = Task(description='Task 2', priority=2)
        self.baby_agi.add_task(task1)
        self.baby_agi.add_task(task2)
        self.baby_agi.print_next_task()
        assert capsys.readouterr().out.strip() == '*****NEXT TASK*****\nTask 1'

    def test_print_task_result(self, capsys):
        description = 'Complete objective'
        priority = 1
        task = Task(description=description, priority=priority)
        self.baby_agi.add_task(task)
        result = 'Task completed successfully!'
        self.baby_agi.print_task_result(result)
        assert capsys.readouterr().out.strip() == '*****TASK RESULT*****\nTask completed successfully!'

class TestBabyAGIAgent:
    @pytest.fixture(autouse=True)
    def set_up(self):
        self.baby_agi = BabyAGI(objective='Solve world hunger.')
        self.agent = BabyAGIAgent(self.baby_agi, objective='Solve world hunger.')

    def test_process_prompt(self):
        result = self.agent.process_prompt()
        assert result == 'Task completed successfully!'
        assert len(self.baby_agi.task_list) == 1
        assert self.baby_agi.task_list[0].description == 'Solve world hunger.'
        assert self.baby_agi.objective == 'Solve world hunger.'

class TestBabyAGIWithToolsAgent:
    @pytest.fixture(autouse=True)
    def set_up(self):
        self.baby_agi = BabyAGI(objective='Solve world hunger.')
        self.agent = BabyAGIWithToolsAgent(self.baby_agi, objective='Solve world hunger.')

    def test_process_prompt(self):
        result = self.agent.process_prompt()
        assert result == 'Task completed successfully!'
        assert len(self.baby_agi.task_list) == 1
        assert self.baby_agi.task_list[0].description == 'Solve world hunger.'
        assert self.baby_agi.objective == 'Solve world hunger.'
        assert self.baby_agi.tools == ['tools']

class TestBabyAgi:
    @pytest.fixture(autouse=True)
    def set_up(self):
        self.baby_agi = BabyAGI(objective='Solve world hunger.')

    def test_baby_agi_properties(self):
        assert self.baby_agi.objective == 'Solve world hunger.'
        assert self.baby_agi.task_list == []

    def test_add_task(self):
        description = 'Complete objective'
        priority = 1
        task = Task(description=description, priority=priority)
        self.baby_agi.add_task(task)
        assert len(self.baby_agi.task_list) == 1
        assert self.baby_agi.task_list[0].description == description

    def test_prioritize_tasks(self):
        task1 = Task(description='Task 1', priority=1)
        task2 = Task(description='Task 2', priority=2)
        task3 = Task(description='Task 3', priority=3)
        self.baby_agi.add_task(task1)
        self.baby_agi.add_task(task2)
        self.baby_agi.add_task(task3)
        prioritized_tasks = self.baby_agi.prioritize_tasks()
        assert len(prioritized_tasks) == 3
        assert prioritized_tasks[0].description == 'Task 3'
        assert prioritized_tasks[1].description == 'Task 2'
        assert prioritized_tasks[2].description == 'Task 1'

    def test_execute_task(self):
        description = 'Complete objective'
        priority = 1
        task = Task(description=description, priority=priority)
        self.baby_agi.add_task(task)
        result = self.baby_agi.execute_task()
        assert result == description
        assert len(self.baby_agi.task_list) == 0

    def test_print_task_info(self, capsys):
        task1 = Task(description='Task 1', priority=1)
        task2 = Task(description='Task 2', priority=2)
        self.baby_agi.add_task(task1)
        self.baby_agi.add_task(task2)
        self.baby_agi.print_task_info()
        assert capsys.readouterr().out.strip() == '*****TASK LIST*****\nTask 1\nTask 2\n\n*****NEXT TASK*****\nTask 1'

    def test_print_task_list(self, capsys):
        task1 = Task(description='Task 1', priority=1)
        task2 = Task(description='Task 2', priority=2)
        self.baby_agi.add_task(task1)
        self.baby_agi.add_task(task2)
        self.baby_agi.print_task_list()
        assert capsys.readouterr

    def test_print_next_task(self, capsys):
        task1 = Task(description='Task 1', priority=1)
        task2 = Task(description='Task 2', priority=2)
        self.baby_agi.add_task(task1)
        self.baby_agi.add_task(task2)
        self.baby_agi.print_next_task()
        assert capsys.readouterr().out.strip() == '*****NEXT TASK*****\nTask 1'

    def test_print_task_result(self, capsys):
        description = 'Complete objective'
        priority = 1
        task = Task(description=description, priority=priority)
        self.baby_agi.add_task(task)
        result = 'Task completed successfully!'
        self.baby_agi.print_task_result(result)
        assert capsys.readouterr().out.strip() == '*****TASK RESULT*****\nTask completed successfully!'

    def test_get_agent(self):
        objective = 'Solve world hunger.'
        agent = self.baby_agi.get_agent(objective)
        assert isinstance(agent, BabyAGIAgent)
        assert agent.baby_agi == self.baby_agi
        assert agent.objective == objective

        objective = 'Solve world hunger with tools.'
        agent = self.baby_agi.get_agent(objective)
        assert isinstance(agent, BabyAGIWithToolsAgent)
        assert agent.baby_agi == self.baby_agi
        assert agent.objective == objective

class TestBabyAGIWithToolsController:
    @pytest.fixture(autouse=True)
    def set_up(self):
        self.baby_agi = BabyAGI(objective='Solve world hunger with tools.')
        self.agent = BabyAGIWithToolsAgent(self.baby_agi, objective='Solve world hunger with tools.')

    def test_process_prompt(self):
        result = self.agent.process_prompt()
        assert result == 'Task completed successfully!'
        assert len(self.baby_agi.task_list) == 1
        assert self.baby_agi.task_list[0].description == 'Solve world hunger with tools.'
        assert self.baby_agi.objective == 'Solve world hunger with tools.'
        assert self.baby_agi.tools == ['tools']