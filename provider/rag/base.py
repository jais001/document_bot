from abc import ABC, abstractmethod
from typing import Iterable
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.vectorstores import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from operator import itemgetter
from dotenv import load_dotenv

from prompts import PROMPT_TEMPLATE, PROMPT_TEMPLATE_WITH_HISTORY

load_dotenv()


class Base(ABC):
    """Base Class
    """
    def __init__(
        self, model: dict,
        chunking_config: dict,
        persist_directory="./storage/vectorstore"
    ):
        self.store = {}
        self.model = model
        self.chunking_config = chunking_config
        self.persist_directory = persist_directory
        self.vector_db = None
        self.embedding_model = self.__create_embedding_model(model_name=model.embedding_model)

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

    def ingest_data(self, documents: Iterable[Document]):
        """
        Ingests data into the vector store.

        Args:
            documents (list of str): List of documents to ingest.
        """
        self.__initialize_vector_db()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunking_config['chunk_size'],
            chunk_overlap=self.chunking_config['chunk_overlap']
        )
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
        """Creates a chat chain."""
        llm = self.create_llm()
        retriever=self.vector_db.as_retriever()
        question_answer_chain=create_stuff_documents_chain(llm, PROMPT_TEMPLATE)
        rag_chain=create_retrieval_chain(retriever, question_answer_chain)
        response=rag_chain.invoke({"input":query})
        answer = response['answer']

        return answer

    def get_session_history(self, session_ids):
        print(f"[Conversation Session ID]: {session_ids}")
        if session_ids not in self.store:  # If the session ID is not in the store
            # Create a new ChatMessageHistory object and save it to the store
            self.store[session_ids] = ChatMessageHistory()
        return self.store[session_ids]

    def chat_with_history(self, query: str, session_id: str):
        """Creates a conversational chain."""
        llm = self.create_llm()
        chain = ({
            "context": itemgetter("question") | self.vector_db.as_retriever(),
            "question": itemgetter("question"),
            "chat_history": itemgetter("chat_history"),
                }
                | PROMPT_TEMPLATE_WITH_HISTORY
                | llm
                | StrOutputParser()
            )
        # Create a RAG chain that records conversations
        rag_with_history = RunnableWithMessageHistory(
            chain,
            self.get_session_history,  # Function to retrieve session history
            input_messages_key="question",  # Key for the template variable that will contain the user's question
            history_messages_key="chat_history",  # Key for the history messages
        )
        response = rag_with_history.invoke(
            # Input question
            {"question": query},
            # Record the conversation based on the session ID.
            config={"configurable": {"session_id": session_id}},
        )
        return response      

    # def _format_docs(self, docs: List[Document]) -> str:
    #     """method to format docs

    #     Args:
    #         docs (Document): document objects

    #     Returns:
    #         str: returns joined document as a string
    #     """
    #     return "\n\n".join(doc.page_content for doc in docs)
