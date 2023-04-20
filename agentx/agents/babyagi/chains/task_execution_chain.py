# agentx/agents/babyagi/chains/task_execution_chain.py

from langchain import LLMChain, PromptTemplate
from langchain.llms import BaseLLM


class TaskExecutionChain(LLMChain):
    """A specialized LLMChain for executing tasks based on a given objective,
    context of completed tasks, and a specific task.
    """

    @classmethod
    def from_llm(cls, llm: BaseLLM, verbose: bool = True) -> LLMChain:
        """Create a TaskExecutionChain instance using a BaseLLM language model.

        Args:
            llm (BaseLLM): A language model instance from the langchain.llms module.
            verbose (bool, optional): If True, prints detailed information during
                                      chain execution. Defaults to True.

        Returns:
            LLMChain: A TaskExecutionChain object for executing tasks based on the
                      given information.
        """
        execution_template = (
            "You are an AI who performs one task based on the following objective: {objective}."
            " Take into account these previously completed tasks: {context}."
            " Your task: {task}."
            " Response:"
        )
        prompt = PromptTemplate(
            template=execution_template,
            input_variables=["objective", "context", "task"],
        )
        return cls(prompt=prompt, llm=llm, verbose=verbose)
