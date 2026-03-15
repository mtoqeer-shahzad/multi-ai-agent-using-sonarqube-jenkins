from dotenv import load_dotenv
import os

# .env file se API keys load karo
load_dotenv()


class Settings:
    # Groq API Key
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")

    # Tavily API Key
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY")

    # Allowed Models List
    ALLOWED_MODEL_NAMES = [
        "llama-3.3-70b-versatile",
        "llama-3.3-70b-specdec",
    ]


# Global instance — poori project mein import karo
settings = Settings()