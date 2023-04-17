from langchain import LLMChain, PromptTemplate
from langchain.llms import BaseLLM


class TaskPrioritizationChain(LLMChain):
    """A specialized LLMChain for prioritizing tasks based on a given
    list of task names, an ultimate objective, and the starting task ID.
    """

    @classmethod
    def from_llm(cls, llm: BaseLLM, verbose: bool = True) -> LLMChain:
        """Create a TaskPrioritizationChain instance using a BaseLLM language
        model.

        Args:
            llm (BaseLLM): A language model instance from the langchain.llms module.
            verbose (bool, optional): If True, prints detailed information during chain
                                      execution. Defaults to True.

        Returns:
            LLMChain: A TaskPrioritizationChain object for prioritizing tasks based on
                      the given information.
        """
        task_prioritization_template = (
            "You are an task prioritization AI tasked with cleaning"
            " the formatting of and reprioritizing the following tasks:"
            " {task_names}. Consider the ultimate objective of your team:"
            " {objective}. Do not remove any tasks. Return the result as"
            " a numbered list, like:"
            " #. First task"
            " #. Second task"
            " Start the task list with number {next_task_id} and increase "
            " the number by one for every further task."
            " Make sure to reason about a good order of task to archive the"
            " global objective."
        )
        prompt = PromptTemplate(
            template=task_prioritization_template,
            input_variables=["task_names", "next_task_id", "objective"],
        )
        return cls(prompt=prompt, llm=llm, verbose=verbose)
