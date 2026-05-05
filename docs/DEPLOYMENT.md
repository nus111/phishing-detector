# Deployment Guide

## Prerequisites

- Docker & Docker Compose installed
- Git
- (Optional) GPU for faster ML inference

## Local Development

```bash
# 1. Clone
git clone https://github.com/nus111/phishing-detector.git
cd phishing-detector

# 2. Configure
cp .env.example .env
# Edit .env with your settings

# 3. Start
docker-compose up -d

# 4. Access
# Frontend:  http://localhost:3000
# Backend:   http://localhost:8000
# API Docs:  http://localhost:8000/docs
# ML Service: http://localhost:8001
```

## Services

| Service | Port | Description |
|---------|------|-------------|
| frontend | 3000 | Next.js web application |
| backend | 8000 | FastAPI REST API |
| ml-service | 8001 | ML model inference |
| db | 5432 | PostgreSQL database |

## Environment Variables

See `.env.example` for all available configuration options.

## Production Deployment

### Option 1: Vercel + Railway
- Deploy frontend to Vercel
- Deploy backend + ML to Railway
- Use managed PostgreSQL (e.g., Supabase, Neon)

### Option 2: Cloud VM
- Use any cloud VM (AWS EC2, GCP, DigitalOcean)
- Install Docker + Docker Compose
- Configure nginx reverse proxy
- Set up SSL with Let's Encrypt

### Option 3: School Server
- Follow school IT guidelines
- Request necessary ports and permissions

## Database Migrations

```bash
# Generate migration
cd backend
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

## Monitoring

- Health check endpoints:
  - Backend: `GET /health`
  - ML Service: `GET /health`
- Logs: `docker-compose logs -f [service]`
