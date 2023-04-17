from typing import Dict, List

from langchain import LLMChain
from langchain.vectorstores import FAISS


def _get_top_tasks(vectorstore: FAISS, query: str, k: int) -> List[str]:
    """Get the top k tasks based on the similarity to the given query.

    Args:
        vectorstore (FAISS): A vector store instance for searching tasks.
        query (str): A text query representing the information to be matched with tasks.
        k (int): The number of top tasks to retrieve.

    Returns:
        List[str]: A list of top tasks, sorted by similarity to the query.
    """
    results = vectorstore.similarity_search_with_score(query, k=k)
    if not results:
        return []
    sorted_results, _ = zip(*sorted(results, key=lambda x: x[1], reverse=True))
    return [str(item.metadata["task"]) for item in sorted_results]


def execute_task(
    vectorstore: FAISS, execution_chain: LLMChain, objective: str, task: str, k: int = 5
) -> str:
    """Execute a given task using the provided execution_chain and context from the vectorstore.

    Args:
        vectorstore (FAISS): A vectorstore instance for searching tasks.
        execution_chain (LLMChain): A language model chain instance for executing tasks.
        objective (str): The overall objective of the task execution.
        task (str): The specific task to be executed.
        k (int, optional): The number of top related tasks to use as context. Defaults to 5.

    Returns:
        str: The result of the executed task.
    """
    context = _get_top_tasks(vectorstore, query=objective, k=k)
    return execution_chain.run(objective=objective, context=context, task=task)


def get_next_task(
    task_creation_chain: LLMChain,
    result: str,
    task_description: str,
    task_list: List[str],
    objective: str,
) -> List[Dict]:
    """Get the next task based on task_creation_chain.

    Args:
        task_creation_chain (LLMChain): A TaskCreationChain instance for generating new tasks.
        result (str): The result of the last completed task.
        task_description (str): The description of the last completed task.
        task_list (List[str]): A list of incomplete tasks.
        objective (str): The overall objective for generating new tasks.

    Returns:
        List[Dict]: A list of dictionaries containing new tasks, with each task represented
                    by a "task_name" key.
    """
    incomplete_tasks = ", ".join(task_list)
    response = task_creation_chain.run(
        result=result,
        task_description=task_description,
        incomplete_tasks=incomplete_tasks,
        objective=objective,
    )
    new_tasks = response.split("\n")
    return [{"task_name": task_name} for task_name in new_tasks if task_name.strip()]


def prioritize_tasks(
    task_prioritization_chain: LLMChain,
    this_task_id: int,
    task_list: List[Dict],
    objective: str,
) -> List[Dict]:
    """Prioritize tasks in the given task_list based on the objective.

    Args:
      task_prioritization_chain (LLMChain): An instance of the TaskPrioritizationChain class.
      this_task_id (int): The current task ID.
      task_list (List[Dict]): A list of dictionaries representing tasks with a "task_name" key.
      objective (str): The overall objective for task prioritization.

    Returns:
      List[Dict]: A list of dictionaries representing prioritized tasks,
                  each with a "task_id" and "task_name" key.
    """
    task_names = [t["task_name"] for t in task_list]
    next_task_id = int(this_task_id) + 1
    response = task_prioritization_chain.run(
        task_names=task_names, next_task_id=next_task_id, objective=objective
    )
    new_tasks = response.split("\n")
    prioritized_task_list = []
    for task_string in new_tasks:
        if not task_string.strip():
            continue
        task_parts = task_string.strip().split(".", 1)
        if len(task_parts) == 2:
            task_id = task_parts[0].strip()
            task_name = task_parts[1].strip()
            prioritized_task_list.append({"task_id": task_id, "task_name": task_name})
    return prioritized_task_list
