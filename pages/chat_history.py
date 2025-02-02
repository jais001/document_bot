import os
import json
import streamlit as st

from constants import *

st.set_page_config(page_title="AI Bot", page_icon=":robot_face:")

saved_chats_container =  st.container()


def read_saved_chat(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            item = json.loads(line)
            data.append(item)
    return data


def format_log_text(saved_contents: list) -> str:
    """Method to format the log text

    Args:
        saved_contents (list): log text

    Returns:
        str: formatted text
    """
    try:
        formatted_lines = []

        for line in saved_contents:
            if line['role'] == 'user':
                formatted_lines.append(f"user: {line['content']}")
            elif line['role'] == 'assistant':
                formatted_lines.append(f"assistant: {line['content']}")

        formatted_text = "\n".join(line for line in formatted_lines)
        return formatted_text
    except Exception as e:
        return f"An error occurred while parsing log text: {str(e)}"


with saved_chats_container:
    save_path = os.path.join(ROOT_DIR, SAVED_CHAT_DIR)
    saved_items = os.listdir(save_path)
    # Filter out files with 0 bytes
    saved_items = [item for item in saved_items if os.path.getsize(os.path.join(save_path, item)) > 0]
    # Sort the remaining files based on their modification time (newest first)
    saved_items.sort(key=lambda x: os.path.getmtime(os.path.join(save_path, x)), reverse=True)
    select_chat = st.selectbox(
        "Saved Chats:",
        saved_items,
        index=None,
        placeholder="Select a Chat...",
    )

    if select_chat:
        saved_contents = read_saved_chat(os.path.join(save_path, select_chat))
        formatted_text = format_log_text(saved_contents)
        st.write("<p style='font-size:14px;'>Log Text:</p>", unsafe_allow_html=True)
        st.write("<p style='font-size:18px;color: red;'>Manual edits to the log text will not be saved.</p>",
                 unsafe_allow_html=True)
        txt = st.text_area(
        "Log Text",
        formatted_text,
        height=500,
        label_visibility="hidden"
        )
