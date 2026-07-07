import os
import json
from dotenv import load_dotenv
from pipeline import answer_question
from retriever import HybridRetriever

load_dotenv()


def run_evaluation(dataset_path: str = "evals/golden_dataset.json"):
    with open(dataset_path, "r") as f:
        dataset = json.load(f)

    print(f"📊 Running evaluation on {len(dataset)} questions...\n")

    # Load retriever once for all questions
    retriever = HybridRetriever()
    results = []

    for i, item in enumerate(dataset):
        question = item["question"]
        ground_truth = item["ground_truth"]

        print(f"[{i+1}/{len(dataset)}] {question[:60]}...")

        output = answer_question(question, retriever)

        results.append({
            "question": question,
            "ground_truth": ground_truth,
            "generated_answer": output["answer"],
            "sources": output["sources"],
            "chunks": [{"text": c["text"], "source": c["source"]} for c in output["chunks"]],
        })

        print(f"  ✅ Done\n")

    os.makedirs("evals", exist_ok=True)
    output_path = "evals/eval_results.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"💾 Results saved to {output_path}")
    print(f"Total questions evaluated: {len(results)}")
    return results


if __name__ == "__main__":
    run_evaluation()