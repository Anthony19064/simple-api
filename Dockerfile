# Base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy requirement file (ถ้ามี) หรือ install Flask ตรงๆ
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY app.py .

# Expose port
EXPOSE 5000

# Run app
CMD ["python", "app.py"]
