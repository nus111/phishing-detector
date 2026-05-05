# Model Documentation

## Model Architecture

**Base Model:** `xlm-roberta-base` (550M parameters, supports 100+ languages)

**Task:** Binary text classification (legitimate vs phishing)

**Fine-tuning:** Custom fine-tuned on multilingual phishing datasets

## Training Data

| Language | Source | Samples |
|----------|--------|---------|
| English | PhishTank, APWG, SpamAssassin | TBD |
| Chinese | CNNIC, Tencent Security | TBD |
| Malay | Synthetic (translated) | TBD |
| Tamil | Synthetic (translated) | TBD |

## Performance Targets

| Language | Precision | Recall | F1-Score |
|----------|-----------|--------|----------|
| English  | ≥ 0.90   | ≥ 0.85 | ≥ 0.87  |
| Chinese  | ≥ 0.85   | ≥ 0.80 | ≥ 0.82  |
| Malay    | ≥ 0.80   | ≥ 0.75 | ≥ 0.77  |
| Tamil    | ≥ 0.80   | ≥ 0.75 | ≥ 0.77  |

## Model Versions

| Version | Date | Description |
|---------|------|-------------|
| placeholder-v1.0 | 2026-05 | Rule-based placeholder |
| v1.0 | TBD | First fine-tuned model |

## Limitations

- Performance may degrade on languages with limited training data
- May not detect highly novel phishing techniques
- Does not analyze images or attachments
- Real-time API integration with messaging platforms is not supported

## Retraining

Model can be retrained via the admin dashboard or CLI:
```bash
python ml/training/train_xlmr.py --data ml/data/processed/train.jsonl --epochs 5
```
