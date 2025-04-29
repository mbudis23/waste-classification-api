FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies untuk OpenCV
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0

# Copy requirements dan install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy semua file project
COPY . .

# Expose port
EXPOSE 8001

# Jalankan server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
