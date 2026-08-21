FROM python:3.10-slim

WORKDIR /app

# Install system C/C++ libraries for OpenCV, Tesseract OCR, and PDF processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    poppler-utils \
    libgl1 \
    libglib2.0-0 \
    libxcb1 \
    libx11-xcb1 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5001

CMD ["python", "app.py"]
