import os
import streamlit as st
from st_pages import get_nav_from_toml
from streamlit_extras.switch_page_button import switch_page

from constants import *

st.set_page_config(page_title="AI Bot", page_icon=":robot_face:")

get_nav_from_toml('pages.toml')


st.write("# AI Bot")

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(SAVED_CHAT_DIR, exist_ok=True)
# st.sidebar.success("Select the tab above.")

st.markdown(
    """

    **Chatbot Features:**

    1. User can chat with the AI Bot.
    2. User can view the saved Chat history from the Chat logs [Under Implementation]. 
    
"""
)
st.markdown(" ")
st.markdown(" ")
goto_chatbot = st.button(label="Goto AI Bot")
if goto_chatbot:
    switch_page("AI Bot")
