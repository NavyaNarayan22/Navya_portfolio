import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from rank_bm25 import BM25Okapi
import cohere
from config import cfg

load_dotenv()


class HybridRetriever:
    def __init__(self):
        print("Loading embedding model...")
        self.embeddings = SentenceTransformer(cfg.embedding_model)
        self.qdrant = QdrantClient(url=cfg.qdrant_url)
        self.cohere = cohere.Client(cfg.cohere_api_key)
        self._bm25 = None
        self._all_chunks = None
        print("✅ Retriever ready!")

    def _load_all_chunks(self):
        if self._all_chunks is not None:
            return
        print("Building BM25 index...")
        results, _ = self.qdrant.scroll(
            collection_name=cfg.collection_name,
            limit=10000,
            with_payload=True,
            with_vectors=False,
        )
        self._all_chunks = [r.payload for r in results]
        tokenized = [c["text"].lower().split() for c in self._all_chunks]
        self._bm25 = BM25Okapi(tokenized)
        print(f"✅ BM25 index built over {len(self._all_chunks)} chunks")

    def dense_search(self, query: str, top_k: int = None) -> list[dict]:
        top_k = top_k or cfg.top_k_dense
        query_vector = self.embeddings.encode(query).tolist()
        results = self.qdrant.query_points(
            collection_name=cfg.collection_name,
            query=query_vector,
            limit=top_k,
            with_payload=True,
        ).points
        return [
            {"text": r.payload["text"], "source": r.payload["source"], "score": r.score}
            for r in results
        ]

    def bm25_search(self, query: str, top_k: int = None) -> list[dict]:
        top_k = top_k or cfg.top_k_dense
        self._load_all_chunks()
        tokenized_query = query.lower().split()
        scores = self._bm25.get_scores(tokenized_query)
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
        return [
            {"text": self._all_chunks[i]["text"], "source": self._all_chunks[i]["source"], "score": float(scores[i])}
            for i in top_indices
        ]

    def reciprocal_rank_fusion(self, dense_results: list, bm25_results: list, k: int = 60) -> list[dict]:
        scores = {}
        docs = {}
        for rank, doc in enumerate(dense_results):
            key = doc["text"][:100]
            scores[key] = scores.get(key, 0) + 1 / (k + rank + 1)
            docs[key] = doc
        for rank, doc in enumerate(bm25_results):
            key = doc["text"][:100]
            scores[key] = scores.get(key, 0) + 1 / (k + rank + 1)
            docs[key] = doc
        sorted_keys = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
        return [docs[k] for k in sorted_keys]

    def rerank(self, query: str, candidates: list[dict], top_n: int = None) -> list[dict]:
        top_n = top_n or cfg.top_k_rerank
        if not candidates:
            return []
        docs = [c["text"] for c in candidates]
        response = self.cohere.rerank(
            model=cfg.cohere_rerank_model,
            query=query,
            documents=docs,
            top_n=top_n,
        )
        reranked = []
        for r in response.results:
            candidate = candidates[r.index].copy()
            candidate["rerank_score"] = r.relevance_score
            reranked.append(candidate)
        return reranked

    def retrieve(self, query: str) -> list[dict]:
        print(f"\n🔍 Query: {query}")
        dense = self.dense_search(query)
        print(f"  Dense results: {len(dense)}")
        bm25 = self.bm25_search(query)
        print(f"  BM25 results: {len(bm25)}")
        fused = self.reciprocal_rank_fusion(dense, bm25)
        print(f"  After fusion: {len(fused)}")
        reranked = self.rerank(query, fused)
        print(f"  After reranking: {len(reranked)}")
        return reranked