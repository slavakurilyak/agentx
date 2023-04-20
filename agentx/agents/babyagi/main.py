# agentx/agents/babyagi/main.py

from typing import Optional

from langchain import OpenAI

from agentx.agents.babyagi.baby_agi import BabyAGI
from agentx.memory.faiss import FAISSRetriever


def run_baby_agi():
    suggested_objective = "Write a weather report for Vancouver, Canada, today"
    user_objective = input(
        f"What is your objective? (Press enter to use the suggested objective: "
        f"'{suggested_objective}') "
    )

    if not user_objective:
        objective = suggested_objective
    else:
        objective = user_objective

    vectorstore = FAISSRetriever().vectorstore
    llm = OpenAI(temperature=0)

    verbose = False

    max_iterations: Optional[int] = 3
    baby_agi = BabyAGI.from_llm(
        llm=llm,
        vectorstore=vectorstore,
        verbose=verbose,
        max_iterations=max_iterations,
    )

    baby_agi({"objective": objective})


if __name__ == "__main__":
    run_baby_agi()
