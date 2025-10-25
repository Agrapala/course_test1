FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir flask psycopg2-binary requests python-dotenv

EXPOSE 5000
CMD ["python", "app.py"]
