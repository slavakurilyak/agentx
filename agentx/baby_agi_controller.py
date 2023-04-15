from typing import List

class Task:
    def __init__(self, description: str, priority: int, objective: str):
        self.description = description
        self.priority = priority
        self.objective = objective

class BabyAGI:
    def __init__(self):
        self.task_list = []
        self.tools = []

    def add_task(self, task: Task):
        self.task_list.append(task)

    def prioritize_tasks(self):
        return sorted(self.task_list, key=lambda task: task.priority, reverse=True)

    def execute_task(self):
        if len(self.task_list) == 0:
            return None
        task = self.task_list.pop(0)
        return task.description

    def print_task_info(self):
        self.print_task_list()
        self.print_next_task()

    def print_task_list(self):
        print('\n*****TASK LIST*****')
        for task in self.task_list:
            print(task.description)

    def print_next_task(self):
        if len(self.task_list) > 0:
            next_task = self.task_list[0]
            print('\n*****NEXT TASK*****')
            print(next_task.description)
        else:
            print('\n*****NO TASKS REMAINING*****')

    def print_task_result(self, result):
        print('\n*****TASK RESULT*****')
        print(result)

    def get_agent(self, objective):
        if 'tools' in objective:
            print('Using BabyAGIWithToolsAgent for objective:', objective)
            return BabyAGIWithToolsAgent(self, objective)
        else:
            print('Using BabyAGIAgent for objective:', objective)
            return BabyAGIAgent(self, objective)

class Agent:
    def __init__(self, objective):
        self.objective = objective

    def process_prompt(self):
        pass

class BabyAGIAgent(Agent):
    def __init__(self, baby_agi):
        super().__init__(baby_agi.objective)
        self.baby_agi = baby_agi

    def process_prompt(self):
        task_description = self.objective
        self.baby_agi.add_task(Task(description=task_description, priority=1))
        self.baby_agi.objective = self.objective
        return 'Task completed successfully!'

class BabyAGIWithToolsAgent(Agent):
    def __init__(self, baby_agi):
        super().__init__(baby_agi.objective)
        self.baby_agi = baby_agi

    def process_prompt(self):
        self.baby_agi.tools.append('tools')
        task_description = self.objective
        self.baby_agi.add_task(Task(description=task_description, priority=1))
        self.baby_agi.objective = self.objective
        return 'Task completed successfully!'

def main():
    objective = input("Enter objective: ")
    baby_agi = BabyAGI()
    baby_agi.objective = objective
    agent = baby_agi.get_agent(objective)
    result = agent.process_prompt()
    baby_agi.print_task_result(result)

if __name__ == '__main__':
    main()
