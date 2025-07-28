FROM python:3.10-slim

# --- Install system dependencies ---
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    poppler-utils \
    git \
    && rm -rf /var/lib/apt/lists/*

# --- Set working directory ---
WORKDIR /app

# --- Copy app files ---
COPY app/ /app/

# --- Copy model and input PDFs ---
COPY models/ /app/models/
COPY Collection/ /app/Collection/

# --- Install Python dependencies ---
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# --- Set entry point to shell script ---
RUN chmod +x run_pipeline.sh
CMD ["bash", "run_pipeline.sh"]
