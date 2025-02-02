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
        model_engine = config.llm.engine
        model = config[model_engine]
        chunking_config = config.chunk_config

        if model_engine == OPENAI_MODEL:
            pass
            # rag_model = OpenAIRAGService()
            return rag_model
        elif model_engine == GROQ_MODEL:
            config = config.groq
            rag_model = GroqRAGService(
                model=model, chunking_config=chunking_config
            )
            return rag_model
        else:
            raise NotImplementedError("Model currently not implemented")
