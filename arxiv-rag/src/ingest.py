import os
import hashlib
from pathlib import Path
from dotenv import load_dotenv
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from config import cfg

load_dotenv()


def extract_text_from_pdf(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def chunk_text(text: str, source: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=cfg.chunk_size,
        chunk_overlap=cfg.chunk_overlap,
        separators=["\n\n", "\n", ". ", " "],
    )
    return splitter.create_documents([text], metadatas=[{"source": source}])


def get_chunk_id(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()


def ingest_papers(papers_dir: str = "data/papers"):
    embeddings = SentenceTransformer(cfg.embedding_model)
    client = QdrantClient(url=cfg.qdrant_url)

    existing = [c.name for c in client.get_collections().collections]
    if cfg.collection_name in existing:
        client.delete_collection(cfg.collection_name)
        print("🗑️  Deleted old collection")

    client.create_collection(
        collection_name=cfg.collection_name,
        vectors_config=VectorParams(size=cfg.embedding_dim, distance=Distance.COSINE),
    )
    print(f"✅ Created collection: {cfg.collection_name}")

    pdf_files = list(Path(papers_dir).glob("*.pdf"))
    print(f"\n📄 Found {len(pdf_files)} papers\n")

    for pdf_path in pdf_files:
        print(f"Processing: {pdf_path.name}")
        text = extract_text_from_pdf(str(pdf_path))
        if not text.strip():
            print("  ⚠️  Skipping — no text extracted")
            continue

        chunks = chunk_text(text, source=pdf_path.name)
        print(f"  📦 {len(chunks)} chunks")

        batch_size = 50
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            texts = [c.page_content for c in batch]
            vectors = embeddings.encode(texts).tolist()
            points = [
                PointStruct(
                    id=get_chunk_id(texts[j]),
                    vector=vectors[j],
                    payload={"text": texts[j], "source": batch[j].metadata["source"]}
                )
                for j in range(len(batch))
            ]
            client.upsert(collection_name=cfg.collection_name, points=points)

        print("  ✅ Done\n")

    print("🎉 Ingestion complete!")


if __name__ == "__main__":
    ingest_papers()