"""Configuration module for Quantum Knowledge Weaver (QKW).
Manages system settings, API keys, URLs, and runtime parameters.
"""

import os
from typing import List, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"


class Settings(BaseModel):
    # App Settings
    app_name: str = "Quantum Knowledge Weaver (QKW)"
    app_version: str = "0.1.0"
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))

    # LLM Settings (Multi-Provider Support: DeepSeek, Gemini, Groq, OpenAI, Ollama)
    llm_provider: str = os.getenv("LLM_PROVIDER", "auto")  # 'auto', 'deepseek', 'gemini', 'groq', 'openai', 'ollama'
    deepseek_api_key: Optional[str] = os.getenv("DEEPSEEK_API_KEY", None)
    deepseek_base_url: str = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    deepseek_model: str = os.getenv("DEEPSEEK_MODEL", "deepseek-reasoner")  # 'deepseek-reasoner' (R1) or 'deepseek-chat' (V3)
    gemini_api_key: Optional[str] = os.getenv("GEMINI_API_KEY", os.getenv("GOOGLE_API_KEY", None))
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    groq_api_key: Optional[str] = os.getenv("GROQ_API_KEY", None)
    groq_model: str = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY", None)
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "deepseek-r1:latest")
    ollama_fallback_model: str = os.getenv("OLLAMA_FALLBACK_MODEL", "llama3.1")
    llm_temperature: float = float(os.getenv("LLM_TEMPERATURE", "0.2"))
    llm_timeout_seconds: float = float(os.getenv("LLM_TIMEOUT_SECONDS", "45.0"))

    # Quantum Router Settings
    quantum_backend: str = os.getenv("QUANTUM_BACKEND", "simulator")  # 'simulator' or 'ibm_quantum'
    ibm_quantum_token: Optional[str] = os.getenv("IBM_QUANTUM_TOKEN", None)
    qaoa_p_steps: int = int(os.getenv("QAOA_P_STEPS", "1"))
    max_apis_to_select: int = int(os.getenv("MAX_APIS_TO_SELECT", "4"))

    # Vector Memory (Qdrant)
    qdrant_url: Optional[str] = os.getenv("QDRANT_URL", None)  # None triggers local in-memory
    qdrant_collection: str = os.getenv("QDRANT_COLLECTION", "qkw_queries")

    # Knowledge Graph (Neo4j)
    neo4j_uri: Optional[str] = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    neo4j_user: str = os.getenv("NEO4J_USER", "neo4j")
    neo4j_password: str = os.getenv("NEO4J_PASSWORD", "password")

    # API Timeouts and Rate Limits (seconds)
    api_timeout_seconds: float = float(os.getenv("API_TIMEOUT_SECONDS", "10.0"))
    api_max_retries: int = int(os.getenv("API_MAX_RETRIES", "2"))


settings = Settings()
