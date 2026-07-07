import os
import json
from dotenv import load_dotenv
from groq import Groq
from config import cfg

load_dotenv()

client = Groq(api_key=cfg.groq_api_key)


def llm_score(prompt: str) -> float:
    """Ask Llama to score something 0-1 and return the float."""
    response = client.chat.completions.create(
        model=cfg.groq_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=10,
    )
    text = response.choices[0].message.content.strip()
    try:
        score = float(text)
        return max(0.0, min(1.0, score))
    except ValueError:
        # If model returns something like "0.8 " or "Score: 0.8"
        for token in text.replace(",", ".").split():
            try:
                return max(0.0, min(1.0, float(token)))
            except ValueError:
                continue
        return 0.0


def score_faithfulness(answer: str, contexts: list[str]) -> float:
    """Is the answer grounded in the retrieved context?"""
    context_text = "\n\n".join(contexts)
    prompt = f"""You are an evaluator. Given the context and an answer, score how faithful the answer is to the context.
A score of 1.0 means every claim in the answer is supported by the context.
A score of 0.0 means the answer contains claims not found in the context.

Context:
{context_text[:3000]}

Answer:
{answer}

Respond with ONLY a decimal number between 0.0 and 1.0. No explanation."""
    return llm_score(prompt)


def score_answer_relevancy(question: str, answer: str) -> float:
    """Does the answer actually address the question?"""
    prompt = f"""You are an evaluator. Score how well the answer addresses the question.
A score of 1.0 means the answer directly and completely answers the question.
A score of 0.0 means the answer is completely irrelevant to the question.

Question: {question}

Answer: {answer}

Respond with ONLY a decimal number between 0.0 and 1.0. No explanation."""
    return llm_score(prompt)


def score_context_precision(question: str, contexts: list[str]) -> float:
    """Are the retrieved chunks relevant to the question?"""
    relevant = 0
    for ctx in contexts:
        prompt = f"""Is the following context relevant to answering this question?
Question: {question}
Context: {ctx[:500]}

Answer with ONLY 1 (relevant) or 0 (not relevant). No explanation."""
        score = llm_score(prompt)
        if score >= 0.5:
            relevant += 1
    return relevant / len(contexts) if contexts else 0.0


def score_context_recall(ground_truth: str, contexts: list[str]) -> float:
    """Does the retrieved context contain the information needed for the ground truth?"""
    context_text = "\n\n".join(contexts)
    prompt = f"""You are an evaluator. Given the context and a reference answer, score how much of the reference answer's information is present in the context.
A score of 1.0 means all information needed to produce the reference answer is in the context.
A score of 0.0 means none of the needed information is in the context.

Context:
{context_text[:3000]}

Reference Answer:
{ground_truth}

Respond with ONLY a decimal number between 0.0 and 1.0. No explanation."""
    return llm_score(prompt)


def run_custom_eval(results_path: str = "evals/eval_results.json"):
    with open(results_path, "r") as f:
        results = json.load(f)

    print(f"📊 Scoring {len(results)} results with custom LLM evaluator...\n")

    all_scores = {
        "faithfulness": [],
        "answer_relevancy": [],
        "context_precision": [],
        "context_recall": [],
    }

    for i, r in enumerate(results):
        question = r["question"]
        answer = r["generated_answer"]
        ground_truth = r["ground_truth"]
        contexts = [c["text"] for c in r.get("chunks", [])]

        print(f"[{i+1}/{len(results)}] {question[:60]}...")

        f_score = score_faithfulness(answer, contexts)
        ar_score = score_answer_relevancy(question, answer)
        cp_score = score_context_precision(question, contexts)
        cr_score = score_context_recall(ground_truth, contexts)

        all_scores["faithfulness"].append(f_score)
        all_scores["answer_relevancy"].append(ar_score)
        all_scores["context_precision"].append(cp_score)
        all_scores["context_recall"].append(cr_score)

        print(f"  Faithfulness:      {f_score:.2f}")
        print(f"  Answer Relevancy:  {ar_score:.2f}")
        print(f"  Context Precision: {cp_score:.2f}")
        print(f"  Context Recall:    {cr_score:.2f}\n")

    summary = {k: round(sum(v) / len(v), 3) for k, v in all_scores.items()}

    print("=" * 40)
    print("🏆 FINAL SCORES")
    print("=" * 40)
    print(f"  Faithfulness:      {summary['faithfulness']:.3f}")
    print(f"  Answer Relevancy:  {summary['answer_relevancy']:.3f}")
    print(f"  Context Precision: {summary['context_precision']:.3f}")
    print(f"  Context Recall:    {summary['context_recall']:.3f}")
    print("=" * 40)

    with open("evals/baseline_scores.json", "w") as f:
        json.dump(summary, f, indent=2)

    print("\n💾 Scores saved to evals/baseline_scores.json")
    return summary


if __name__ == "__main__":
    run_custom_eval()