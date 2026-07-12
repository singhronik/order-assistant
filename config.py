import os
from dotenv import load_dotenv

load_dotenv()

# Base URL of your Django Order Management System API (see the
# order-management-system project). Must be running for tools to work.
DJANGO_API_BASE_URL = os.environ.get("DJANGO_API_BASE_URL", "http://127.0.0.1:8000/api")

# Which LLM provider to use: "gemini", "anthropic", or "openai"
LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "gemini")

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
