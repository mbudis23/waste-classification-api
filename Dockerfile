# Gunakan base image Python 3.10 yang ringan
FROM python:3.10-slim

# Install dependensi sistem untuk image processing dan torch
RUN apt-get update && apt-get install -y \
    libglib2.0-0 libsm6 libxext6 libxrender-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Buat direktori kerja di dalam container
WORKDIR /app

# Salin semua file proyek (kecuali yang di .dockerignore)
COPY . .

# Upgrade pip dan install dependensi dari requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Expose port untuk FastAPI
EXPOSE 8000

# Perintah untuk menjalankan API FastAPI
CMD ["uvicorn", "main:app" , "--reload", "--port", "8000"]
