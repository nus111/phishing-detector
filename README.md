# 🛡️ Phishing Detector

AI-Based Phishing & Fraud Detection System — Capstone Project (GRP09)

## Overview

A multilingual AI-powered system that detects phishing and fraud messages in real-time, with special focus on protecting non-English speaking vulnerable populations (refugees, migrant workers, international students) in Malaysia.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React + Next.js + Tailwind CSS |
| Backend | Python FastAPI |
| Database | PostgreSQL |
| AI/ML | XLM-RoBERTa (Hugging Face Transformers) |
| Deployment | Docker + Docker Compose |

## Quick Start

```bash
# Clone the repository
git clone https://github.com/nus111/phishing-detector.git
cd phishing-detector

# Copy environment config
cp .env.example .env
# Edit .env with your settings

# Start all services
docker-compose up -d

# Access:
# Frontend:  http://localhost:3000
# Backend:   http://localhost:8000
# ML Service: http://localhost:8001
# API Docs:  http://localhost:8000/docs
```

## Project Structure

```
phishing-detector/
├── frontend/          # Next.js frontend application
├── backend/           # FastAPI backend server
├── ml/                # ML model training & inference
├── docs/              # Project documentation
├── docker-compose.yml # Service orchestration
└── .env.example       # Environment variables template
```

## Team

| Name | Role |
|------|------|
| Yang Jintao | Group Leader, Frontend Developer |
| Lin Yubo | Security & Backend Engineer |
| Liu Zeyu | Lead Data Engineer |
| Li Hao | Data Engineer |
| Yang Junxi | ML/AI Engineer |

## Supervisor

Dr. Arafat Mohammed Rashad Al-dhaqm

## License

This project is for academic purposes (Taylor's University Capstone Project).
