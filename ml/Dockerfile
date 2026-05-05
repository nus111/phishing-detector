# ═══════════════════════════════════════════════
# ML Service — Optimized for minimal size
# Uses CPU-only PyTorch (~800MB vs ~2.5GB full)
# ═══════════════════════════════════════════════

# ── Stage 1: Install dependencies ──
FROM python:3.11-slim AS builder

WORKDIR /build

# System deps for building wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ && \
    rm -rf /var/lib/apt/lists/*

# Install Python deps with CPU-only PyTorch
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    -r requirements.txt

# ── Stage 2: Runtime (minimal) ──
FROM python:3.11-slim AS runtime

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Only install curl for healthcheck (no gcc/build tools)
RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Copy app code
COPY app/ ./app/

# Expose port
EXPOSE 8001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

# Run
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
