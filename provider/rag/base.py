from abc import ABC, abstractmethod
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from dotenv import load_dotenv

from prompts import PROMPT_TEMPLATE

load_dotenv()


class Base(ABC):
    """Base Class
    """
    def __init__(self, llm_model_name, persist_directory="./storage/vectorstore"):
        self.llm_model_name = llm_model_name
        self.persist_directory = persist_directory
        self.vector_db = None
        self.embedding_model = self.__create_embedding_model()

    def __create_embedding_model(self, model_name="all-MiniLM-L6-v2"):
        """Create the embedding model."""
        embeddings=HuggingFaceEmbeddings(model_name=model_name)
        return embeddings

    def __initialize_vector_db(self):
        """Initializes the vector database."""
        if not self.vector_db:
            self.vector_db = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embedding_model,
            )

    def ingest_data(self, documents):
        """
        Ingests data into the vector store.

        Args:
            documents (list of str): List of documents to ingest.
        """
        self.__initialize_vector_db()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        splitted_documents = text_splitter.split_documents(documents)
        self.vector_db.add_documents(splitted_documents)
        self.vector_db.persist()

    def delete_file(self, file_path: str):
        """deletes an ingested file from vector db

        Args:
            vector_db: vector DB
            file_path (str): file path
        """
        doc_ids = self.vector_db.get(where={"source": file_path})["ids"]
        if doc_ids:
            self.vector_db.delete(doc_ids)

    @abstractmethod
    def create_llm(self):
        """Create the LLM object for the service."""

    def chat(self, query: str):
        """Creates a conversational retrieval chain."""
        llm = self.create_llm()
        retriever=self.vector_db.as_retriever()
        question_answer_chain=create_stuff_documents_chain(llm, PROMPT_TEMPLATE)
        rag_chain=create_retrieval_chain(retriever, question_answer_chain)
        response=rag_chain.invoke({"input":query})
        answer = response['answer']

        return answer

    # def _format_docs(self, docs: List[Document]) -> str:
    #     """method to format docs

    #     Args:
    #         docs (Document): document objects

    #     Returns:
    #         str: returns joined document as a string
    #     """
    #     return "\n\n".join(doc.page_content for doc in docs)
