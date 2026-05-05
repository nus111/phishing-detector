"""
Model Evaluation Script

Evaluates the trained model on test data, computes per-language metrics.

Usage:
    python evaluate.py --model ../models/xlm-roberta-phishing --data ../data/processed/test.jsonl
"""

import argparse
import json
import os


def evaluate(model_path: str, test_data_path: str):
    """
    Evaluate model performance.
    
    Metrics per language:
    - Precision
    - Recall
    - F1-Score
    - Accuracy
    
    Returns dict of metrics.
    """
    # TODO: Implement evaluation
    # from transformers import pipeline
    # classifier = pipeline("text-classification", model=model_path, return_all_scores=True)
    #
    # results = {"en": [], "zh": [], "ms": [], "ta": []}
    # with open(test_data_path) as f:
    #     for line in f:
    #         sample = json.loads(line)
    #         pred = classifier(sample["text"])
    #         results[sample["language"]].append(...)
    
    metrics = {
        "overall": {"precision": 0.0, "recall": 0.0, "f1": 0.0, "accuracy": 0.0},
        "en": {"precision": 0.0, "recall": 0.0, "f1": 0.0},
        "zh": {"precision": 0.0, "recall": 0.0, "f1": 0.0},
        "ms": {"precision": 0.0, "recall": 0.0, "f1": 0.0},
        "ta": {"precision": 0.0, "recall": 0.0, "f1": 0.0},
    }
    return metrics


def main():
    parser = argparse.ArgumentParser(description="Evaluate phishing detection model")
    parser.add_argument("--model", required=True, help="Path to trained model")
    parser.add_argument("--data", required=True, help="Path to test data (JSONL)")
    args = parser.parse_args()

    print(f"Evaluating model: {args.model}")
    print(f"Test data: {args.data}")
    print("=" * 50)

    metrics = evaluate(args.model, args.data)

    for lang, scores in metrics.items():
        print(f"\n[{lang.upper()}]")
        for metric, value in scores.items():
            print(f"  {metric}: {value:.4f}")

    # Save results
    output_path = os.path.join(os.path.dirname(args.model), "evaluation_results.json")
    with open(output_path, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"\nResults saved to {output_path}")


if __name__ == "__main__":
    main()
