from langchain_groq import ChatGroq
from provider.rag.base import Base


class GroqRAGService(Base):
    """Groq service
    """
    def __init__(self, llm_model_name: str, persist_directory="./storage/vectorstore"):
        super().__init__(llm_model_name, persist_directory)

    def create_llm(self):
        """Creates the Groq LLM object."""
        chat_model = ChatGroq(model=self.llm_model_name, temperature=0)
        return chat_model
