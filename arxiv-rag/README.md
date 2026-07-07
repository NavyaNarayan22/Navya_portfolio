# ArXiv Research Assistant — Hybrid RAG System

A production-grade **Retrieval-Augmented Generation** system that answers questions over 10 landmark ML research papers. Built to demonstrate the full ML engineering loop: build → evaluate → iterate → quantify improvements.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-serving-green?style=flat&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red?style=flat&logo=streamlit)
![Qdrant](https://img.shields.io/badge/Qdrant-vector--store-purple?style=flat)

---

## UI Preview 

<img width="1920" height="1080" alt="Screenshot 2026-07-07 155308" src="https://github.com/user-attachments/assets/967ea8a6-8c31-4b09-85a9-acabc1082b1d" />


## Demo

> **Q:** What is the key innovation in the Transformer architecture?
>
> **A:** The key innovation is self-attention, which allows the model to relate different positions of a sequence to compute a representation, replacing recurrence entirely.
>
> **Sources:** `attention_is_all_you_need` · `t5`

---

## Evaluation Results

Custom **LLM-as-judge** evaluator using Llama 3.1 via Groq API, measuring 4 RAGAS-style metrics across 10 golden Q&A pairs.

| Metric | Baseline | Improved | Δ |
|---|---|---|---|
| Faithfulness | 0.08 | **0.76** | +0.68 ✅ |
| Answer Relevancy | 0.61 | **0.66** | +0.05 ✅ |
| Context Precision | 0.64 | **0.98** | +0.34 ✅ |
| Context Recall | 0.10 | **0.59** | +0.49 ✅ |

**Key insight:** Baseline scores were low because golden dataset questions referenced papers not present in the corpus. Fixing corpus-dataset alignment produced the improvement — demonstrating that eval dataset quality is as critical as model quality.

---

## Architecture

```
User Query
    │
    ▼
Hybrid Retriever
    ├── Dense Search (Qdrant + all-MiniLM-L6-v2)
    └── BM25 Search (rank-bm25)
         │
         ▼
    Reciprocal Rank Fusion
         │
         ▼
    Cohere Reranking
         │
         ▼
    Top-5 Relevant Chunks
         │
         ▼
    LLM Generation (Llama 3.1 8B via Groq)
         │
         ▼
    Final Answer
```

---

## Papers in Corpus

| Paper | File |
|---|---|
| Attention Is All You Need (Transformer) | `attention_is_all_you_need.pdf` |
| BERT | `bert.pdf` |
| RAG — Retrieval Augmented Generation | `rag_original.pdf` |
| Dense Passage Retrieval (DPR) | `dense_passage_retrieval.pdf` |
| RoBERTa | `roberta.pdf` |
| InstructGPT | `instructgpt.pdf` |
| GPT-3 | `gpt3.pdf` |
| T5 | `t5.pdf` |
| RLHF | `rlhf.pdf` |
| LLaMA | `llama.pdf` |

---

## Tech Stack

| Component | Technology |
|---|---|
| Vector Store | Qdrant (Docker) |
| Embeddings | `all-MiniLM-L6-v2` (HuggingFace, local) |
| Keyword Search | BM25 (rank-bm25) |
| Fusion | Reciprocal Rank Fusion |
| Reranking | Cohere Rerank API |
| LLM | Llama 3.1 8B via Groq API |
| Evaluation | Custom LLM-as-judge |
| API | FastAPI |
| UI | Streamlit |

---

## Project Structure

```
arxiv-rag/
├── src/
│   ├── ingest.py            # PDF parsing, chunking, embedding, Qdrant upload
│   ├── retriever.py         # Hybrid retriever (dense + BM25 + rerank)
│   ├── pipeline.py          # End-to-end query → retrieve → generate
│   ├── evaluator.py         # Runs golden dataset through pipeline
│   ├── evaluator_custom.py  # LLM-as-judge scoring
│   ├── app.py               # FastAPI serving layer
│   ├── ui.py                # Streamlit frontend
│   └── config.py            # Centralized config
├── evals/
│   ├── golden_dataset.json      # 10 hand-crafted Q&A pairs
│   ├── eval_results.json        # Pipeline outputs
│   ├── baseline_scores.json     # Pre-fix scores
│   └── improved_scores.json     # Post-fix scores
├── requirements.txt
└── .env                         # API keys (gitignored)
```

---

## Setup

```bash
# 1. Clone and install
git clone https://github.com/NavyaNarayan22/Navya_portfolio.git
cd Navya_portfolio/arxiv-rag
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# 2. Create .env file
QDRANT_URL=http://localhost:6333
COLLECTION_NAME=arxiv_papers
GROQ_API_KEY=your_groq_key
COHERE_API_KEY=your_cohere_key

# 3. Start Qdrant
docker run -d --name qdrant -p 6333:6333 qdrant/qdrant

# 4. Ingest papers
python src/download_papers.py
python src/ingest.py

# 5. Run FastAPI (Terminal 1)
cd src
python -m uvicorn app:app --reload --port 8000

# 6. Run Streamlit (Terminal 2)
streamlit run src/ui.py
```

Open **http://localhost:8501**

---

## Built by

**Navya Narayan Panicker** · [LinkedIn](https://linkedin.com/in/navyapanicker) · [GitHub](https://github.com/NavyaNarayan22)
