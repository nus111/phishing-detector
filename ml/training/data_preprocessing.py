"""
Data Preprocessing Pipeline

Converts raw phishing datasets into a unified JSONL format for training.

Output format (each line):
{
    "text": "Message content",
    "label": 0,       // 0=legitimate, 1=phishing
    "language": "en",  // en|zh|ms|ta
    "phishing_type": "visa_threat|fake_job|gov_impersonation|other",
    "source": "dataset_name"
}

Usage:
    python data_preprocessing.py --input ../data/raw --output ../data/processed
"""

import argparse
import json
import os
import re


def clean_text(text: str) -> str:
    """Clean and normalize text."""
    text = re.sub(r'<[^>]+>', '', text)       # Remove HTML tags
    text = re.sub(r'\s+', ' ', text)           # Normalize whitespace
    text = text.strip()
    return text


def process_phishtank(input_path: str, output_path: str):
    """Process PhishTank dataset."""
    # TODO: Implement PhishTank data processing
    pass


def process_chinese_dataset(input_path: str, output_path: str):
    """Process Chinese phishing dataset."""
    # TODO: Implement Chinese data processing
    pass


def augment_data(input_path: str, output_path: str):
    """
    Data augmentation strategies:
    - Back translation (en->zh->en)
    - Synonym replacement
    - LLM-generated synthetic samples
    """
    # TODO: Implement augmentation
    pass


def split_dataset(input_path: str, output_dir: str, train_ratio=0.7, val_ratio=0.15):
    """Split processed data into train/val/test sets."""
    # TODO: Implement dataset splitting
    print(f"Splitting {input_path} -> train/val/test ({train_ratio}/{val_ratio}/{1-train_ratio-val_ratio})")


def main():
    parser = argparse.ArgumentParser(description="Preprocess phishing datasets")
    parser.add_argument("--input", required=True, help="Raw data directory")
    parser.add_argument("--output", required=True, help="Processed output directory")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)
    print(f"Processing data from {args.input} -> {args.output}")
    print("Preprocessing pipeline (placeholder)")


if __name__ == "__main__":
    main()
