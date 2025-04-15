FROM python:3.11-slim

WORKDIR /app

# Set PYTHONPATH to include the current directory
ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
