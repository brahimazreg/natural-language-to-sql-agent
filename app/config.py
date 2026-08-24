from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_host: str
    database_port: int = 5433
    database_name: str
    database_user: str
    database_password: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


settings = Settings()

# =========================
# API Keys
# =========================

#GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# =========================
# File paths
# =========================

#DATA_FILE_PATH = Path("data/raw")
#VECTOR_STORE_PATH = Path("data/faiss_index")

# =========================
# RAG configuration
# =========================

#CHUNK_SIZE = 500
#CHUNK_OVERLAP = 20

#TOP_K_RESULT = 5

# =========================
# LLM configuration
# =========================

#LLM_MODEL_NAME = "models/gemini-3.5-flash-lite"

#EMBEDDING_MODEL_NAME = "gemini-embedding-001"

# =========================
# Prompt
# =========================

#PROMPT = """
#"""

# =========================
# Validation
# =========================

#def check_api_key():
    #"""Stop early with a clear message if the Gemini API key is missing."""

    #if not GEMINI_API_KEY:
        #raise ValueError(
            #"Missing GEMINI_API_KEY. "
            #"Please add it to your .env file."
        #)# """