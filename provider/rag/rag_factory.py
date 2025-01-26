from provider.rag.base import Base
from provider.rag.groq import GroqRAGService
# from provider.rag.openai import OpenAIRAGService
from constants import *


class RagFactory:
    """Factory for generating the rag model
    """
    def __init__(self):
        pass

    @staticmethod
    def create(config: dict) -> Base:
        """Method for creating the rag model

        Args:
            model (str): model for creation
        """
        rag_model = None
        model = config.llm.engine

        if model == OPENAI_MODEL:
            pass
            # rag_model = OpenAIRAGService()
            return rag_model
        elif model == GROQ_MODEL:
            config = config.groq
            rag_model = GroqRAGService(llm_model_name=config.chat_model)
            return rag_model
        else:
            raise NotImplementedError("Model currently not implemented")
