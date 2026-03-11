import os
from dotenv import load_dotenv

load_dotenv()

# ==============================
# ENVIRONMENT
# ==============================

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

if ENVIRONMENT not in ["development", "production"]:
    raise ValueError("ENVIRONMENT must be 'development' or 'production'")

IS_PRODUCTION = ENVIRONMENT == "production"


# ==============================
# API KEYS
# ==============================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not configured.")

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))


# ==============================
# MODEL CONFIGURATION
# ==============================

LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

MAX_QUERY_LENGTH = int(os.getenv("MAX_QUERY_LENGTH", 1000))
MAX_CONTEXT_CHARS = int(os.getenv("MAX_CONTEXT_CHARS", 12000))
MAX_PROMPT_TOTAL_CHARS = int(os.getenv("MAX_PROMPT_TOTAL_CHARS", 15000))


# ==============================
# FEATURE FLAGS
# ==============================

ENABLE_EVALUATION = os.getenv("ENABLE_EVALUATION", "false").lower() == "true"
HALLUCINATION_STRICT_MODE = os.getenv("HALLUCINATION_STRICT_MODE", "false").lower() == "true"


# ==============================
# PRODUCTION SAFETY OVERRIDES
# ==============================

if IS_PRODUCTION:
    ENABLE_EVALUATION = False