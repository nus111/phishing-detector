"""
XLM-RoBERTa Phishing Detection — Training Script

Usage:
    python train_xlmr.py --data ../data/processed/train.jsonl --epochs 5

Requirements:
    pip install transformers datasets torch scikit-learn
"""

import argparse
import json
import os

# TODO: Uncomment and implement after data is ready
# from transformers import (
#     XLMRobertaForSequenceClassification,
#     XLMRobertaTokenizer,
#     Trainer,
#     TrainingArguments,
# )
# from datasets import load_dataset
# from sklearn.metrics import precision_recall_fscore_support


def load_data(data_path: str):
    """Load JSONL dataset."""
    # TODO: Implement data loading
    # Each line: {"text": "...", "label": 0|1, "language": "en|zh|ms|ta"}
    pass


def compute_metrics(eval_pred):
    """Compute precision, recall, F1 for evaluation."""
    # TODO: Implement metrics
    # predictions, labels = eval_pred
    # preds = predictions.argmax(axis=-1)
    # precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='binary')
    # return {"precision": precision, "recall": recall, "f1": f1}
    pass


def main():
    parser = argparse.ArgumentParser(description="Train XLM-RoBERTa for phishing detection")
    parser.add_argument("--data", required=True, help="Path to training data (JSONL)")
    parser.add_argument("--output", default="../models/xlm-roberta-phishing", help="Output model path")
    parser.add_argument("--epochs", type=int, default=5, help="Number of training epochs")
    parser.add_argument("--batch_size", type=int, default=16, help="Batch size")
    parser.add_argument("--lr", type=float, default=2e-5, help="Learning rate")
    parser.add_argument("--model_name", default="xlm-roberta-base", help="Base model name")
    args = parser.parse_args()

    print(f"Training config: {vars(args)}")
    print("=" * 50)

    # TODO: Implement training pipeline
    # 1. Load tokenizer and model
    # tokenizer = XLMRobertaTokenizer.from_pretrained(args.model_name)
    # model = XLMRobertaForSequenceClassification.from_pretrained(
    #     args.model_name, num_labels=2
    # )
    #
    # 2. Load and tokenize dataset
    # dataset = load_data(args.data)
    #
    # 3. Set up training arguments
    # training_args = TrainingArguments(
    #     output_dir=args.output,
    #     num_train_epochs=args.epochs,
    #     per_device_train_batch_size=args.batch_size,
    #     learning_rate=args.lr,
    #     evaluation_strategy="epoch",
    #     save_strategy="epoch",
    #     load_best_model_at_end=True,
    #     metric_for_best_model="f1",
    # )
    #
    # 4. Train
    # trainer = Trainer(
    #     model=model,
    #     args=training_args,
    #     train_dataset=train_dataset,
    #     eval_dataset=eval_dataset,
    #     compute_metrics=compute_metrics,
    # )
    # trainer.train()
    #
    # 5. Save
    # model.save_pretrained(args.output)
    # tokenizer.save_pretrained(args.output)

    print("Training complete! (placeholder)")


if __name__ == "__main__":
    main()
