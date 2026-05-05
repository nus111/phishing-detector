<div align="center">

# 🛡️ Phishing Detector

**AI-Based Phishing & Fraud Detection System**

[![CI](https://github.com/nus111/phishing-detector/actions/workflows/ci.yml/badge.svg)](https://github.com/nus111/phishing-detector/actions/workflows/ci.yml)

**🌐 [English](README.md) | [中文](README_zh.md) | [Bahasa Melayu](README_ms.md) | [தமிழ்](README_ta.md)**

</div>

---

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

## Features

- 🔍 **Real-time Message Analysis** — Paste any message to check for phishing indicators
- 🌍 **Multilingual Support** — English, 中文, Bahasa Melayu, தமிழ்
- ⚠️ **Risk Assessment** — Color-coded risk levels (Low / Medium / High) with detailed explanations
- 📚 **Security Education** — Tips, articles, and quizzes to improve phishing awareness
- 📊 **Admin Dashboard** — Threat trends, language distribution, user analytics
- 🤖 **AI-Powered** — XLM-RoBERTa deep learning model for accurate detection

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
# Frontend:   http://localhost:3000
# Backend:    http://localhost:8000
# ML Service: http://localhost:8001
# API Docs:   http://localhost:8000/docs
```

## Project Structure

```
phishing-detector/
├── frontend/          # Next.js frontend (React + Tailwind + i18n)
├── backend/           # FastAPI backend (REST API + JWT auth)
├── ml/                # ML model training & inference service
├── docs/              # API, Model, Deployment documentation
├── docker-compose.yml # Service orchestration
└── .env.example       # Environment variables template
```

## API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/auth/register` | Register | ❌ |
| POST | `/api/v1/auth/login` | Login | ❌ |
| GET | `/api/v1/auth/me` | Current user | 🔒 |
| POST | `/api/v1/analyze` | Analyze message | 🔒 |
| GET | `/api/v1/analyze/history` | Analysis history | 🔒 |
| GET | `/api/v1/education` | Education content | ❌ |
| POST | `/api/v1/education/quiz/submit` | Submit quiz | 🔒 |
| GET | `/api/v1/admin/dashboard` | Admin stats | 👑 |

> Full API documentation available at `http://localhost:8000/docs` (Swagger UI)

## Team

| Name | Role | Responsibilities |
|------|------|-----------------|
| Yang Jintao | Group Leader, Frontend | UI/UX, website development, project management |
| Lin Yubo | Security & Backend | REST API, database, security, deployment |
| Liu Zeyu | Lead Data Engineer | Data preprocessing, feature extraction, model evaluation |
| Li Hao | Data Engineer | Data collection, cleaning, AI model tuning |
| Yang Junxi | ML/AI Engineer | Model selection, fine-tuning, error analysis |

## Supervisor

**Dr. Arafat Mohammed Rashad Al-dhaqm**
School of Computer Science, Taylor's University

## License

This project is for academic purposes — Taylor's University Capstone Project (PRJ63504).
