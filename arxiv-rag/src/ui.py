import streamlit as st
import requests
import time

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="ArXiv Research Assistant",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    background-color: #0a0a0f;
    color: #e2e8f0;
}

.stApp {
    background-color: #0a0a0f;
}

/* Header */
.header-container {
    padding: 3rem 0 2rem 0;
    border-bottom: 1px solid #1e2a3a;
    margin-bottom: 2.5rem;
}

.header-eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    color: #4ade80;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}

.header-title {
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 2.6rem;
    font-weight: 300;
    color: #f1f5f9;
    line-height: 1.15;
    margin-bottom: 0.5rem;
}

.header-title span {
    font-weight: 500;
    color: #ffffff;
}

.header-sub {
    font-size: 0.9rem;
    color: #64748b;
    font-weight: 300;
    margin-top: 0.5rem;
}

/* Paper pills */
.pill-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin-top: 1rem;
}

.pill {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    padding: 0.2rem 0.6rem;
    border: 1px solid #1e3a2f;
    border-radius: 2px;
    color: #4ade80;
    background: #0d1f16;
    letter-spacing: 0.05em;
}

/* Input */
.stTextInput > div > div > input {
    background-color: #0f1623 !important;
    border: 1px solid #1e2a3a !important;
    border-radius: 4px !important;
    color: #e2e8f0 !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
}

.stTextInput > div > div > input:focus {
    border-color: #4ade80 !important;
    box-shadow: 0 0 0 2px rgba(74, 222, 128, 0.1) !important;
}

.stTextInput > div > div > input::placeholder {
    color: #334155 !important;
}

/* Button */
.stButton > button {
    background-color: #4ade80 !important;
    color: #0a0a0f !important;
    border: none !important;
    border-radius: 4px !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    padding: 0.65rem 1.5rem !important;
    letter-spacing: 0.02em !important;
    transition: all 0.15s ease !important;
}

.stButton > button:hover {
    background-color: #86efac !important;
    transform: translateY(-1px) !important;
}

/* Answer card */
.answer-card {
    background: #0f1623;
    border: 1px solid #1e2a3a;
    border-left: 3px solid #4ade80;
    border-radius: 4px;
    padding: 1.5rem 1.75rem;
    margin: 1.5rem 0 1rem 0;
    font-size: 0.95rem;
    line-height: 1.75;
    color: #cbd5e1;
}

/* Question display */
.question-display {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    color: #4ade80;
    margin-bottom: 0.75rem;
    letter-spacing: 0.03em;
}

/* Sources */
.sources-header {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    color: #475569;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 1rem;
    margin-bottom: 0.5rem;
}

.source-tag {
    display: inline-block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    padding: 0.2rem 0.55rem;
    background: #0d1a2a;
    border: 1px solid #1e3352;
    border-radius: 2px;
    color: #60a5fa;
    margin-right: 0.35rem;
    margin-bottom: 0.35rem;
}

/* History divider */
.history-divider {
    border: none;
    border-top: 1px solid #0f1623;
    margin: 2rem 0;
}

/* Metric bar */
.metric-row {
    display: flex;
    gap: 1.5rem;
    margin-bottom: 2rem;
    flex-wrap: wrap;
}

.metric-box {
    background: #0f1623;
    border: 1px solid #1e2a3a;
    border-radius: 4px;
    padding: 0.75rem 1.25rem;
    min-width: 130px;
}

.metric-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    color: #475569;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.25rem;
}

.metric-value {
    font-size: 1.4rem;
    font-weight: 500;
    color: #4ade80;
}

/* Hide streamlit chrome */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.block-container {
    padding-top: 0 !important;
    max-width: 860px !important;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-container">
    <div class="header-eyebrow">RAG · Hybrid Retrieval · LLM-as-Judge Eval</div>
    <div class="header-title">ArXiv <span>Research Assistant</span></div>
    <div class="header-sub">10 landmark ML papers · Dense + BM25 + Cohere reranking · Llama 3.1 generation</div>
    <div class="pill-row">
        <span class="pill">Transformer</span>
        <span class="pill">BERT</span>
        <span class="pill">RAG</span>
        <span class="pill">DPR</span>
        <span class="pill">RoBERTa</span>
        <span class="pill">GPT-3</span>
        <span class="pill">InstructGPT</span>
        <span class="pill">T5</span>
        <span class="pill">RLHF</span>
        <span class="pill">LLaMA</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Eval scores
st.markdown("""
<div class="metric-row">
    <div class="metric-box">
        <div class="metric-label">Faithfulness</div>
        <div class="metric-value">0.76</div>
    </div>
    <div class="metric-box">
        <div class="metric-label">Relevancy</div>
        <div class="metric-value">0.66</div>
    </div>
    <div class="metric-box">
        <div class="metric-label">Precision</div>
        <div class="metric-value">0.98</div>
    </div>
    <div class="metric-box">
        <div class="metric-label">Recall</div>
        <div class="metric-value">0.59</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Session state
if "history" not in st.session_state:
    st.session_state.history = []

# Input row
col1, col2 = st.columns([5, 1])
with col1:
    question = st.text_input(
        label="question",
        label_visibility="collapsed",
        placeholder="e.g. How does BERT differ from the original Transformer?",
        key="question_input"
    )
with col2:
    ask_clicked = st.button("Ask →")

# Example questions
st.markdown("""
<div style="margin-top: 0.5rem; margin-bottom: 1.5rem;">
    <span style="font-family: IBM Plex Mono, monospace; font-size: 0.62rem; color: #334155; letter-spacing: 0.1em; text-transform: uppercase;">Try: </span>
    <span style="font-size: 0.78rem; color: #475569;">What is self-attention? &nbsp;·&nbsp; How does RoBERTa improve BERT? &nbsp;·&nbsp; What is RLHF?</span>
</div>
""", unsafe_allow_html=True)

# Query
if ask_clicked and question.strip():
    with st.spinner(""):
        try:
            start = time.time()
            response = requests.post(
                f"{API_URL}/query",
                json={"question": question},
                timeout=60
            )
            elapsed = round(time.time() - start, 2)
            data = response.json()
            data["elapsed"] = elapsed
            st.session_state.history.insert(0, {
                "question": question,
                "answer": data["answer"],
                "sources": data.get("sources", []),
                "elapsed": elapsed,
            })
        except requests.exceptions.ConnectionError:
            st.error("Cannot reach API. Make sure FastAPI is running on port 8000.")
        except Exception as e:
            st.error(f"Error: {e}")

# History
for item in st.session_state.history:
    sources_html = "".join(
        f'<span class="source-tag">{s.replace(".pdf", "")}</span>'
        for s in sorted(set(item["sources"]))
    )
    st.markdown(f"""
<div class="question-display">› {item['question']}</div>
<div class="answer-card">{item['answer']}</div>
<div class="sources-header">Retrieved from</div>
<div>{sources_html}</div>
<div style="font-family: IBM Plex Mono, monospace; font-size: 0.6rem; color: #1e2a3a; margin-top: 0.5rem;">{item.get('elapsed', '')}s</div>
<hr class="history-divider">
""", unsafe_allow_html=True)

if not st.session_state.history:
    st.markdown("""
<div style="text-align: center; padding: 4rem 0; color: #1e2a3a;">
    <div style="font-family: IBM Plex Mono, monospace; font-size: 0.7rem; letter-spacing: 0.15em;">AWAITING QUERY</div>
</div>
""", unsafe_allow_html=True)