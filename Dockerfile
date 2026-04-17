FROM python:3.12-slim

# Prevent bytecode generation and ensure unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install curl for healthcheck routine
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Non-root user for production safety
RUN addgroup --system appgroup && adduser --system --group appuser

# Cache dependencies layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set permissions for secure execution
RUN chown -R appuser:appgroup /app
USER appuser

EXPOSE 8501

# Container health monitoring
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

CMD ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]