FROM python:3.11-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set environment variables
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# System deps for OpenCV and PyTorch (CPU)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ffmpeg \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender-dev \
        libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies (creates .venv in /app)
RUN uv sync --frozen --no-dev

# Copy application code
COPY . .

# Use the virtual environment created by uv
ENV PATH="/app/.venv/bin:$PATH"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
