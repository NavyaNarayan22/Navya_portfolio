from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

@dataclass
class Config:
    qdrant_url: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    collection_name: str = os.getenv("COLLECTION_NAME", "arxiv_papers")

    embedding_model: str = "all-MiniLM-L6-v2"
    embedding_dim: int = 384

    chunk_size: int = 256
    chunk_overlap: int = 32

    top_k_dense: int = 15
    top_k_rerank: int = 5

    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    groq_model: str = "llama-3.1-8b-instant"
    temperature: float = 0.1
    max_tokens: int = 500

    cohere_api_key: str = os.getenv("COHERE_API_KEY", "")
    cohere_rerank_model: str = "rerank-english-v3.0"

cfg = Config()