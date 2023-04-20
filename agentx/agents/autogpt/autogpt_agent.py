# agentx/agents/autogpt/autogpt_agent.py

from langchain.chat_models import ChatOpenAI
from langchain.experimental import AutoGPT


class AutoGPTAgent:
    def __init__(self, tools, memory):
        self.agent = AutoGPT.from_llm_and_tools(
            ai_name="Tom",
            ai_role="Assistant",
            llm=ChatOpenAI(temperature=0),
            tools=tools,
            memory=memory,
        )

    def run(self, prompts):
        self.agent.run(prompts)
