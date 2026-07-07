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
