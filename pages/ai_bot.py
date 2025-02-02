import os
import uuid
import json
import logging
from dotenv import load_dotenv
import streamlit as st
from streamlit_chat import message
from datetime import datetime


from provider.rag.rag_factory import RagFactory
from service.data_preprocessing_service import DataPreprocessingService
from utils.utils import (
    load_yaml_to_configbox,
    trim_assistant_response,
    generate_user_id,
    configure_logging_by_guid,
)
from constants import *


# Setting page title and header
st.set_page_config(page_title="AI Bot", page_icon=":robot_face:")
st.markdown(
    "<h3 style='text-align: center;'>AI RAG Bot</h3>",
    unsafe_allow_html=True,
)
# Load environment variables
load_dotenv()

config = load_yaml_to_configbox(yaml_file_path=CONFIG_FILE_PATH)
greetings = {"role": "assistant", "content": "Hey, I am you personal AI Bot. Ask me anything from the document."}
greet_user = True

if "rag_model" not in st.session_state:
    st.session_state["rag_model"] = RagFactory().create(config=config)
rag_model = st.session_state["rag_model"]


# Configuration
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Session state initialization
if "user_id" not in st.session_state:
    st.session_state["user_id"] = generate_user_id()
if "chat_answer_history" not in st.session_state:
    st.session_state["chat_answer_history"] = []
if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [greetings]
if "chat_document" not in st.session_state:
    st.session_state["chat_document"] = ""
if "current_session_guid" not in st.session_state:
    st.session_state["current_session_guid"] = str(uuid.uuid4())
    configure_logging_by_guid()  # Configure logging for the new session


# Streamlit app interface
st.sidebar.title("Options")

# Upload document
uploaded_file = st.sidebar.file_uploader("Upload a PDF document", type=["pdf"])

if uploaded_file:
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    if file_path != st.session_state["chat_document"]:
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.session_state["chat_document"] = file_path

        # Ingest file into the vector database
        data_service = DataPreprocessingService()
        documents = data_service.extract_documents(pdf_file_path=file_path)
        rag_model.ingest_data(documents=documents)

        st.sidebar.success(f"Uploaded and processed {uploaded_file.name}.")



st.sidebar.markdown(" ")
st.sidebar.markdown(" ")
# Clear chat and document options
if st.sidebar.button("Clear Chat History"):
    st.session_state["chat_history"] = []
    st.session_state["chat_answer_history"] = []
    st.session_state["user_prompt_history"] = []
    st.sidebar.success("Chat history cleared.")

st.sidebar.markdown(" ")
st.sidebar.markdown(" ")
if st.sidebar.button("Clear Conversation"):
    chat_document_path = st.session_state["chat_document"]
    rag_model.delete_file(file_path=chat_document_path)
    st.session_state["chat_document"] = ""
    st.sidebar.success("Document cleared.")

st.sidebar.markdown(" ")
st.sidebar.markdown(" ")

if st.sidebar.button("Save Conversation"):
    chats = st.session_state["chat_history"][1:]
    datetime_stamp = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
    save_chat_path = os.path.join(SAVED_CHAT_DIR, f"chat_{datetime_stamp}.jsonl")

    if len(chats) > 0:
        with open(save_chat_path, 'w') as file:
            for item in chats:
                json.dump(item, file)
                file.write('\n')


def generate_response(user_query: str) -> str:
    """method to generate openai chatbot response

    Args:
        user_query (str): user query

    Returns:
        str: chatbot response
    """
    st.session_state["chat_history"].append({"role": "user", "content": user_query})

    response = rag_model.chat(query=user_query)

    # # print the token usage
    # usage = completion["usage"]
    # st.session_state["prompt_tokens"] += usage["prompt_tokens"]
    # st.session_state["completion_tokens"] += usage["completion_tokens"]


    if "unsupported" in response.lower():
        response = "I'm sorry, Please ask queries related to the Document."

    logging.info({"role": "user", "content": user_query})
    logging.info({"role": "assistant", "content": response})
    st.session_state["chat_history"].append({"role": "assistant", "content": response})

    return response


# container for chat history
response_container = st.container()
# container for text box
container = st.container()

with container:
    prompt = st.chat_input("Send a message")

    if prompt:
        output = generate_response(prompt)
        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answer_history"].append(output)

with response_container:
    if greet_user:
        message(
            f"<p style='font-size:20px;'>{greetings['content']}</p>",
            key=str(0),
            allow_html=True,
        )

    if st.session_state["chat_answer_history"]:
        chat_history = st.session_state["chat_answer_history"]
        user_history = st.session_state["user_prompt_history"]

        for i, (user_prompt, chat_answer) in enumerate(zip(user_history, chat_history)):
            message(
                f'<p style="font-size:20px;">{user_prompt}</p>',
                is_user=True,
                key=str(i+1) + "_user",
                allow_html=True,
            )
            message(
                f'<p style="font-size:20px;">{chat_answer}</p>',
                key=str(i+1),
                allow_html=True,
            )
