import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
