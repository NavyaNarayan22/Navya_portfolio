import os
from dotenv import load_dotenv
from groq import Groq
from retriever import HybridRetriever
from config import cfg

load_dotenv()

client = Groq(api_key=cfg.groq_api_key)


def build_prompt(query: str, chunks: list[dict]) -> str:
    context = ""
    for i, chunk in enumerate(chunks):
        context += f"\n[Source {i+1}: {chunk['source']}]\n{chunk['text']}\n"

    return f"""You are an expert on machine learning research papers.
Answer the question using ONLY the context provided below.
If the answer is not in the context, say "I don't have enough information to answer this."

Context:
{context}

Question: {query}

Answer:"""


def answer_question(query: str, retriever: HybridRetriever = None) -> dict:
    if retriever is None:
        retriever = HybridRetriever()

    chunks = retriever.retrieve(query)
    prompt = build_prompt(query, chunks)

    response = client.chat.completions.create(
        model=cfg.groq_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=cfg.temperature,
        max_tokens=cfg.max_tokens,
    )

    answer = response.choices[0].message.content

    return {
        "question": query,
        "answer": answer,
        "sources": [c["source"] for c in chunks],
        "chunks": chunks,
    }


if __name__ == "__main__":
    result = answer_question("What is the key innovation in the Transformer architecture?")
    print("\n============================================================")
    print("ANSWER:")
    print(result["answer"])
    print("\nSOURCES:")
    for s in set(result["sources"]):
        print(f"  - {s}")