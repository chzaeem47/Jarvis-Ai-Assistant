import os
from dotenv import load_dotenv


try:
    load_dotenv(override=True)
except Exception as e:
    print(f"[Config] Warning: Could not load .env file: {e}")

class Config:
    """Application configuration"""
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = FLASK_ENV == 'development'
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    CHAT_HISTORY_FILE = '../data/chat_history.json'