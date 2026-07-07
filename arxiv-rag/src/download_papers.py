import os
import urllib.request
import time

# 10 landmark ML papers — great for a portfolio RAG system
papers = [
    # (arxiv_id, friendly_filename)
    ("1706.03762", "attention_is_all_you_need.pdf"),          # Transformer
    ("1810.04805", "bert.pdf"),                                # BERT
    ("2005.11401", "rag_original.pdf"),                        # RAG paper itself!
    ("2108.02035", "dense_passage_retrieval.pdf"),             # DPR
    ("1907.11692", "roberta.pdf"),                             # RoBERTa
    ("2203.02155", "instructgpt.pdf"),                         # InstructGPT
    ("2005.14165", "gpt3.pdf"),                                # GPT-3
    ("1910.10683", "t5.pdf"),                                  # T5
    ("2204.02311", "rlhf.pdf"),                                # RLHF
    ("2302.13971", "llama.pdf"),                               # LLaMA
]

save_dir = os.path.join(os.path.dirname(__file__), "..", "data", "papers")
os.makedirs(save_dir, exist_ok=True)

for arxiv_id, filename in papers:
    url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    save_path = os.path.join(save_dir, filename)

    if os.path.exists(save_path):
        print(f"⏭️  Already exists: {filename}")
        continue

    print(f"⬇️  Downloading {filename}...")
    try:
        urllib.request.urlretrieve(url, save_path)
        print(f"✅ Saved: {filename}")
        time.sleep(2)  # Be polite to arXiv servers
    except Exception as e:
        print(f"❌ Failed {filename}: {e}")

print("\n🎉 Done! Papers are in data/papers/")