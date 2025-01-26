import os
import secrets
from dotenv import load_dotenv
import streamlit as st


from provider.rag.rag_factory import RagFactory
from service.data_preprocessing_service import DataPreprocessingService
from utils.utils import (
    load_yaml_to_configbox,
    trim_assistant_response,
    generate_user_id,
    parse_chat_to_langchain_format,
)
from constants import *

# Load environment variables
load_dotenv()

config = load_yaml_to_configbox(yaml_file_path=CONFIG_FILE_PATH)
rag_model = RagFactory().create(config=config)


# Configuration
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Session state initialization
if "user_id" not in st.session_state:
    st.session_state["user_id"] = generate_user_id()
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "chat_document" not in st.session_state:
    st.session_state["chat_document"] = ""

# Streamlit app interface
st.title("Document Chat Application")
st.sidebar.title("Options")

# Upload document
uploaded_file = st.sidebar.file_uploader("Upload a PDF document", type=["pdf"])

if uploaded_file:
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.session_state["chat_document"] = file_path

    # Ingest file into the vector database
    data_service = DataPreprocessingService()
    documents = data_service.extract_documents(pdf_file_path=file_path)
    rag_model.ingest_data(documents=documents)

    st.sidebar.success(f"Uploaded and processed {uploaded_file.name}.")

# Chat interface
st.header("Chat with your Document")
user_input = st.text_input("Your question:")

if st.button("Send"):
    if user_input:
        # Process chat input
        chat_history = st.session_state["chat_history"]
        chat_answer = rag_model.chat(query=user_input)

        # Update chat history
        st.session_state["chat_history"].append((user_input, chat_answer))

        # Display the chat
        for user_message, assistant_message in st.session_state["chat_history"]:
            st.write(f"**You**: {user_message}")
            st.write(f"**Assistant**: {assistant_message}")
    else:
        st.warning("Please enter a question.")

# Clear chat and document options
if st.sidebar.button("Clear Chat History"):
    st.session_state["chat_history"] = []
    st.sidebar.success("Chat history cleared.")

if st.sidebar.button("Clear Uploaded Document"):
    chat_document_path = st.session_state["chat_document"]
    rag_model.delete_file(file_path=chat_document_path)
    st.session_state["chat_document"] = ""
    st.sidebar.success("Document cleared.")
