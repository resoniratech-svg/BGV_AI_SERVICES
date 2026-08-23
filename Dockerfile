FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=5001 \
    PIP_DEFAULT_TIMEOUT=1000 \
    PIP_RETRIES=20

WORKDIR /app

# Install required system packages for Tesseract OCR, Poppler (PDF conversion), and OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-eng \
    poppler-utils \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install exact authoritative dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --default-timeout=1000 --retries=20 -r requirements.txt

# Copy application source code
COPY . .

EXPOSE 5001

# Run Flask application via Gunicorn WSGI server using deployment wsgi.py entrypoint
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5001} --workers 2 --timeout 180 wsgi:app"]
