from baby_agi import BabyAGIAgent
from baby_agi_with_tools import BabyAGIWithToolsAgent

from typing import List

class Task:
    def __init__(self, description, priority):
        self.description = description
        self.priority = priority

class BabyAGI:
    def __init__(self, objective):
        self.task_list = []
        self.objective = objective
        
    def add_task(self, task: Task):
        self.task_list.append(task)
    
    def prioritize_tasks(self):
        pass
    
    def execute_task(self):
        pass
    
    def print_task_info(self):
        pass
    
    def print_task_list(self):
        print("\n*****TASK LIST*****")
        for t in self.task_list:
            print(t.description)
    
    def print_next_task(self):
        if len(self.task_list) > 0:
            next_task = self.task_list[0]
            print("\n*****NEXT TASK*****")
            print(next_task.description)
        else:
            print("\n*****NO TASKS REMAINING*****")
    
    def print_task_result(self, result: str):
        print("\n*****TASK RESULT*****")
        print(result)
    
    def get_agent(self, objective: str):
        if "tools" in objective:
            print("Using BabyAGIWithToolsAgent for objective:", objective)
            return BabyAGIWithToolsAgent(self, objective)
        else:
            print("Using BabyAGIAgent for objective:", objective)
            return BabyAGIAgent(self, objective)

class Agent:
    def __init__(self, objective: str):
        self.objective = objective
    
    def process_prompt(self):
        pass
    
class BabyAGIAgent(Agent):
    def __init__(self, baby_agi: BabyAGI):
        super().__init__(baby_agi.objective)
        self.baby_agi = baby_agi

    def process_prompt(self):
        self.baby_agi.add_task(Task(description=self.objective, priority=1))
        self.baby_agi.objective = self.objective

        return "Task completed successfully!"

class BabyAGIWithToolsAgent(Agent):
    def __init__(self, baby_agi: BabyAGI):
        super().__init__(baby_agi.objective)
        self.baby_agi = baby_agi

    def process_prompt(self):
        self.baby_agi.tools.append("tools")
        self.baby_agi.add_task(Task(description=self.objective, priority=1))
        self.baby_agi.objective = self.objective

        baby_agi = BabyAGI()
        baby_agi.tools = self.baby_agi.tools
        agent = BabyAGIAgent(baby_agi)
        agent.process_prompt(objective)

        return "Task completed successfully!"

if __name__ == "__main__":
    objective = input("Enter an objective: ")
    print("Using objective:", objective)
    agi = BabyAGI(objective)
    agent = agi.get_agent(objective)
    result = agent.process_prompt()
    agi.print_task_list()
    agi.print_next_task()
    agi.print_task_result(result)
