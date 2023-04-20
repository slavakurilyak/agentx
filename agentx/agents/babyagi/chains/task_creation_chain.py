# agentx/agents/babyagi/chains/task_creation_chain.py

from langchain import LLMChain, PromptTemplate
from langchain.llms import BaseLLM


class TaskCreationChain(LLMChain):
    """A specialized LLMChain for generating new tasks based on a
    specific objective, completed task result, and a list of
    incomplete tasks.
    """

    @classmethod
    def from_llm(cls, llm: BaseLLM, verbose: bool = True) -> LLMChain:
        """Create a TaskCreationChain instance using a BaseLLM language model.

        Args:
            llm (BaseLLM): A language model instance from the langchain.llms module.
            verbose (bool, optional): If True, prints detailed information during
                                      chain execution. Defaults to True.

        Returns:
            LLMChain: A TaskCreationChain object for generating new tasks based on
            the given information.
        """
        task_creation_template = (
            "You are an task creation AI that uses the result of an execution agent"
            " to create new tasks with the following objective: {objective},"
            " The last completed task has the result: {result}."
            " This result was based on this task description: {task_description}."
            " These are incomplete tasks: {incomplete_tasks}."
            " Based on the result, create new tasks to be completed"
            " by the AI system that do not overlap with incomplete tasks."
            " Return the tasks as an array."
        )
        prompt = PromptTemplate(
            template=task_creation_template,
            input_variables=[
                "result",
                "task_description",
                "incomplete_tasks",
                "objective",
            ],
        )
        return cls(prompt=prompt, llm=llm, verbose=verbose)
