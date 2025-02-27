FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y curl net-tools && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY demo_email_service.py .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["python", "-u", "demo_email_service.py"]