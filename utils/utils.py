import os
import yaml
import uuid
import logging
import secrets
from langchain_core.messages import HumanMessage
from box import ConfigBox

from constants import *


def load_yaml_to_configbox(yaml_file_path: str):
    """File to load yaml to configbox
    """
    # Open and read the YAML file
    with open(yaml_file_path, 'r') as file:
        # Parse the YAML file into a Python dictionary
        yaml_data = yaml.safe_load(file)

    # Convert the dictionary into a ConfigBox object
    config = ConfigBox(yaml_data)

    return config


def generate_user_id():
    """
    Generate a unique user identifier using secrets.

    Returns:
        str: A unique user identifier.
    """
    return secrets.token_hex(8)


def trim_assistant_response(response: str) -> str:
    """method to split the response from Assistant part

    Args:
        response (str): response as string

    Returns:
        str: Trimmed response
    """
    # Split the response by "Assistant:"
    parts = response.split("Assistant:")

    if len(parts) == 2:
        return parts[1].strip()
    else:
        return response.strip()


def parse_chat_to_langchain_format(chat_history: list = None) -> list:
    """method to parse chat history to langchain format

    Args:
        chat_history (list, optional): chat history as list. Defaults to None.

    Returns:
        list: Parsed chat history
    """
    chats = []
    for user_input, ai_answer in chat_history:
        chats.append(HumanMessage(content=user_input))
        chats.append(ai_answer)

    return chats


def get_source_link(response: dict) -> str:
    """method to get the source link

    Args:
        response (dict): response as a dict

    Returns:
        str: source link
    """
    if "context" in response and response["context"]:
        source_document_ex = response["context"][0]
        if source_document_ex.metadata:
            metadata = source_document_ex.metadata
            source_link_ex = ""
            if "source" in metadata:
                source_link_ex = metadata["source"]
            else:
                source_link_ex = False
        else:
            source_link_ex = False

    else:
        source_link_ex = False

    if source_link_ex:
        source_documents = source_link_ex
    else:
        source_documents = ""

    return source_documents


def configure_logging_by_guid():
    """Method to perform logging based on guid"""
    unique_guid = str(uuid.uuid4())  # Generate a unique GUID
    log_file = os.path.join(LOG_DIR, f"chat_{unique_guid}.log")

    # Close any existing logging handlers
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logging.basicConfig(
        filename=log_file,
        filemode="w",
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )
