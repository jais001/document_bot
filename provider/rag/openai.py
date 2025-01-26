from langchain.chat_models import ChatOpenAI
from provider.rag.base import Base


class OpenAIRAGService(Base):
    """OpenAI Rag Service
    """
    def __init__(self, embedding_model, vector_db, llm_model_name="gpt-4"):
        super().__init__(embedding_model, vector_db, llm_model_name)

    def create_llm(self):
        """Creates the OpenAI LLM object."""
        return ChatOpenAI(model=self.llm_model_name, temperature=0)
