from langchain_groq import ChatGroq
from provider.rag.base import Base


class GroqRAGService(Base):
    """Groq service
    """
    def __init__(self, model: dict, chunking_config: dict, persist_directory="./storage/vectorstore"):
        super().__init__(model, chunking_config, persist_directory)

    def create_llm(self):
        """Creates the Groq LLM object."""
        chat_model = ChatGroq(model=self.model.chat_model, temperature=0)
        return chat_model
