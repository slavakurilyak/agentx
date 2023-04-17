import pytest
from dotenv import load_dotenv
from langchain.llms import OpenAI

load_dotenv()


@pytest.fixture()
def openai_llm():
    return OpenAI(temperature=0)
