# agentx/memory/faiss.py

from typing import List

import faiss
from dotenv import load_dotenv
from langchain.docstore import InMemoryDocstore
from langchain.docstore.document import Document
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.vectorstores.base import VectorStoreRetriever

load_dotenv()


class FAISSRetriever(VectorStoreRetriever):
    def __init__(self):
        embeddings_model = OpenAIEmbeddings()
        embedding_size = 1536
        index = faiss.IndexFlatL2(embedding_size)
        vectorstore = FAISS(
            embeddings_model.embed_query, index, InMemoryDocstore({}), {}
        )
        super().__init__(vectorstore=vectorstore)

    def get_relevant_documents(self, query: str) -> List[Document]:
        return self.vectorstore.similarity_search(query)
