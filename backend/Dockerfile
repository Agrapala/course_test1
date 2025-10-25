FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install flask psycopg2 requests
EXPOSE 5000
CMD ["python", "app.py"]
