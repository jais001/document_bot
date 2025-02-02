import os

ROOT_DIR = os.getcwd()

UPLOAD_FOLDER = 'uploads'
LOG_DIR = "chatbot_logs"
SAVED_CHAT_DIR = "saved_chats"

PERSIST_DIRECTORY_CHROMA = "db"
PDF_FOLDER_PATH = "static/data"

SIMILARITY_THRESHOLD = 0.7
K_DOCS = 5
TEMPERATURE = 0
MAX_RETRIES = 3

CONFIG_FOLDER = "config"
CONFIG_FILE_PATH = os.path.join(CONFIG_FOLDER, "config.yaml")

substrings = [
    "\x0c",
    "�",
    "\u2003",
    "\u2002",
    "\x08",
    "\u0000",
    "\x07",
    "\n",
    "\t",
    "\r",
    "•",
    "†",
    "¶",
    "‡",
    "‖",
    "§",
    "◼",
    "䡲",
    "⬍",
    "⬇",
    "●",
    "♦",
    "www.triassicsolutions.com",
]


# AI models for RAG
OPENAI_MODEL = "openai"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
GROQ_MODEL = "groq"
