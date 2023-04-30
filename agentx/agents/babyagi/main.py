# agentx/agents/babyagi/main.py

from typing import Optional

from langchain import OpenAI

from agentx.agents.babyagi.baby_agi import BabyAGI
from agentx.memory.faiss import get_faiss_vectorstore_for_openapi


def run_baby_agi():
    OBJECTIVE = "Write a weather report for SF today"

    vectorstore = get_faiss_vectorstore_for_openapi()
    llm = OpenAI(temperature=0)

    # Logging of LLMChains
    verbose = False
    # If None, will keep on going forever
    max_iterations: Optional[int] = 3
    baby_agi = BabyAGI.from_llm(
        llm=llm,
        vectorstore=vectorstore,
        verbose=verbose,
        max_iterations=max_iterations,
    )

    baby_agi({"objective": OBJECTIVE})


if __name__ == "__main__":
    run_baby_agi()
