# AutoGPT
# Implementation of https://github.com/Significant-Gravitas/Auto-GPT but with LangChain primitives (LLMs, PromptTemplates, VectorStores, Embeddings, Tools)

# Set up tools
# We’ll set up an AutoGPT with a search tool, and write-file tool, and a read-file tool

from langchain.utilities import SerpAPIWrapper
from langchain.agents import Tool
from langchain.tools.file_management.write import WriteFileTool
from langchain.tools.file_management.read import ReadFileTool

search = SerpAPIWrapper()
tools = [
    Tool(
        name = "search",
        func=search.run,
        description="useful for when you need to answer questions about current events. You should ask targeted questions"
    ),
    WriteFileTool(),
    ReadFileTool(),
]

# Set up memory
# The memory here is used for the agents intermediate steps

from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
from langchain.embeddings import OpenAIEmbeddings

embeddings_model = OpenAIEmbeddings() # Define your embedding model
import faiss # Initialize the vectorstore as empty

embedding_size = 1536
index = faiss.IndexFlatL2(embedding_size)
vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})

# Setup model and AutoGPT
# Initialize everything using ChatOpenAI model

from langchain.experimental import AutoGPT
from langchain.chat_models import ChatOpenAI

agent = AutoGPT.from_llm_and_tools(
    ai_name="Tom",
    ai_role="Assistant",
    tools=tools,
    llm=ChatOpenAI(temperature=0),
    memory=vectorstore.as_retriever()
)

agent.chain.verbose = True # Set verbose to be true

# Run an example
# Here we will make it write a weather report for SF

agent.run(["write a weather report for SF today"])
