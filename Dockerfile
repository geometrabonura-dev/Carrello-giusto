FROM python:3.12-slim

WORKDIR /tmp

RUN apt-get update \
    && apt-get install -y --no-install-recommends unzip \
    && rm -rf /var/lib/apt/lists/*

COPY carrellogiusto_backend_v7_7_3.zip /tmp/backend.zip

RUN unzip /tmp/backend.zip -d /tmp/extracted \
    && mkdir -p /app \
    && cp -a /tmp/extracted/backend/. /app/

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
