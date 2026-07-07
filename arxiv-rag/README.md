# ArXiv Research Assistant — Hybrid RAG System

A production-grade **Retrieval-Augmented Generation** system that answers questions over 10 landmark ML research papers. Built to demonstrate the full ML engineering loop: build → evaluate → iterate → quantify improvements.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-serving-green?style=flat&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red?style=flat&logo=streamlit)
![Qdrant](https://img.shields.io/badge/Qdrant-vector--store-purple?style=flat)

---

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

User Query
│
▼
┌─────────────────────────────────────┐
│           Hybrid Retriever          │
│  ┌─────────────┐  ┌──────────────┐  │
│  │ Dense Search│  │  BM25 Search │  │
│  │  (Qdrant)   │  │  (rank-bm25) │  │
│  └──────┬──────┘  └──────┬───────┘  │
│         └────────┬────────┘          │
│                  ▼                   │
│       Reciprocal Rank Fusion         │
│                  ▼                   │
│         Cohere Reranking             │
└──────────────────┬──────────────────┘
▼
Top-5 Relevant Chunks
▼
┌──────────────────────────────────────┐
│         LLM Generation               │
│   Llama 3.1 8B via Groq API          │
└──────────────────┬───────────────────┘
▼
Final Answer

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

(venv) PS C:\Users\hp\Navya_portfolio> git push origin main
>>
Enumerating objects: 34, done.
Counting objects: 100% (34/34), done.
Delta compression using up to 12 threads
Compressing objects: 100% (30/30), done.
Writing objects: 100% (33/33), 13.10 MiB | 4.98 MiB/s, done.
Total 33 (delta 2), reused 0 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (2/2), completed with 1 local object.
To https://github.com/NavyaNarayan22/Navya_portfolio.git
   c31e224..fec568e  main -> mainShow moreIt's pushed! 🎉 Go check your GitHub repo at:
github.com/NavyaNarayan22/Navya_portfolio
You should see the arxiv-rag folder there with all your files.
One last thing — write a README. This is what recruiters read first. Want me to write a professional README for:

The top-level portfolio repo (Navya_portfolio/README.md) — intro about you and list of projects
The arxiv-rag project (arxiv-rag/README.md) — architecture, eval scores table, how to run it

Both together make the portfolio look very polished. Should I write them?yesLet me write both. First, what should I put for your bio? Fill in the blanks:

Your role: CS fresher, interning at Happiest Minds as Generative AI developer ✅ (I have this)
Your college name: ?
LinkedIn URL: ?
Any other projects to list besides arxiv-rag?: (e.g. resume parser from internship?)
pdfPerfect, I have everything I need. Let me write both READMEs now.Created 2 files, ran a command, read a fileCreated 2 files, ran a command, read a fileDownload both files. Then:
Place them like this:

portfolio_README.md → rename to README.md and put it in C:\Users\hp\Navya_portfolio\
arxiv_rag_README.md → rename to README.md and put it in C:\Users\hp\Navya_portfolio\arxiv-rag\

Then push:
powershellcd C:\Users\hp\Navya_portfolio
git add .
git commit -m "docs: add portfolio and project READMEs"
git push origin main
Your GitHub will look polished and recruiter-ready! 🎉Arxiv rag readmeDocument · MD Portfolio readmeDocument · MD give it it readme form ill paste it directly from githubHere's the portfolio-level README — paste this directly into GitHub's README editor:

markdown# Navya Narayan Panicker — AI Engineering Portfolio

[![LinkedIn](https://img.shields.io/badge/LinkedIn-navyapanicker-blue?style=flat&logo=linkedin)](https://linkedin.com/in/navyapanicker)
[![GitHub](https://img.shields.io/badge/GitHub-NavyaNarayan22-black?style=flat&logo=github)](https://github.com/NavyaNarayan22)
[![Email](https://img.shields.io/badge/Email-navyanarayanp393@gmail.com-red?style=flat&logo=gmail)](mailto:navyanarayanp393@gmail.com)

---

Final-year Computer Science student at **AMC Engineering College, Bengaluru** (CGPA: 8.5) with hands-on industry experience in Generative AI through internships at **Happiest Minds Technologies** and the **Bharat Unnati AI Fellowship**. I build production-grade AI systems — RAG pipelines, LLM applications, and agentic workflows — and measure what I build with rigorous evaluation frameworks.

**Best Presentation Award** — iThink2025 International Conference &nbsp;|&nbsp; **Published Researcher** — IRJAEH

---

## Projects

### 🔍 [ArXiv Research Assistant — Hybrid RAG System](./arxiv-rag/)
> Production-grade RAG system over 10 landmark ML papers with hybrid retrieval, Cohere reranking, and a custom LLM-as-judge evaluation framework.

| Stack | Eval Scores |
|---|---|
| Qdrant · sentence-transformers · BM25 · Cohere · Groq · FastAPI · Streamlit | Faithfulness **0.76** · Precision **0.98** |

---

## Technical Skills

**AI / ML:** LLMs · RAG · Prompt Engineering · NLP · Neural Networks · Generative AI · Groq · Google Gemini API

**Languages:** Python · Java · C/C++ · JavaScript · SQL · HTML/CSS · React

**Tools:** FastAPI · Streamlit · Qdrant · LangChain · Git · n8n · REST APIs · Agile/Scrum

---

## Experience

**Software Developer Intern — Generative AI** · Happiest Minds Technologies · Feb–May 2026
- Built production RAG chatbots (Resume Parser, PEP Chatbot) deployed for enterprise use
- Engineered prompt pipelines using chain-of-thought and few-shot techniques

**AI Research & Development Intern** · Bharat Unnati AI Fellowship · Jan–May 2026
- Built TalentPulse AI — a 5-agent recruitment intelligence platform using Gemini + n8n

---

*More projects coming soon.*

And here's the arxiv-rag project README:

markdown# ArXiv Research Assistant — Hybrid RAG System

A production-grade **Retrieval-Augmented Generation** system that answers questions over 10 landmark ML research papers. Built to demonstrate the full ML engineering loop: build → evaluate → iterate → quantify improvements.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-serving-green?style=flat&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red?style=flat&logo=streamlit)
![Qdrant](https://img.shields.io/badge/Qdrant-vector--store-purple?style=flat)

---

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
User Query
│
▼
┌─────────────────────────────────────┐
│           Hybrid Retriever          │
│  ┌─────────────┐  ┌──────────────┐  │
│  │ Dense Search│  │  BM25 Search │  │
│  │  (Qdrant)   │  │  (rank-bm25) │  │
│  └──────┬──────┘  └──────┬───────┘  │
│         └────────┬────────┘          │
│                  ▼                   │
│       Reciprocal Rank Fusion         │
│                  ▼                   │
│         Cohere Reranking             │
└──────────────────┬──────────────────┘
▼
Top-5 Relevant Chunks
▼
┌──────────────────────────────────────┐
│         LLM Generation               │
│   Llama 3.1 8B via Groq API          │
└──────────────────┬───────────────────┘
▼
Final Answer

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
└── .env                     # API keys (gitignored)

---

## Setup

```bash
# 1. Clone and install
git clone https://github.com/NavyaNarayan22/Navya_portfolio.git
cd Navya_portfolio/arxiv-rag
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# 2. Create .env
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
