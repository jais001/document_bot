import os
import time
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from constants import *
from provider.preprocessor.preprocessor_factory import PreprocessorFactory


class DataPreprocessingService:
    """Data preprocessing Service"""

    def __init__(self) -> None:
        self.preprocessor = PreprocessorFactory().create()

    def extract_documents(self, pdf_file_path: str) -> None:
        """
        Extract data from PDF documents from the specified folder, processes the text.

        Parameters:
        - pdf_file_path (str): The path to the pdf file.

        Returns:
        - None
        """
        print("data ingestion called!!")
        start_time1 = time.time()  # Record the start time

        loader = PyPDFLoader(pdf_file_path, extract_images=True)
        documents = loader.load()
        end_time1 = time.time()

        # Preprocess the extracted text
        for document in documents:
            text = document.page_content
            preprocessed_text = self.preprocessor.preprocess_document(document_text=text)
            document.page_content = preprocessed_text
            document.metadata = {'source': pdf_file_path}

        print("Document load time:", end_time1-start_time1)
        return documents
