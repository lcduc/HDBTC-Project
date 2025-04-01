FROM python:3.12.3

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY auto_create_topics.py .

CMD ["python", "/app/auto_create_topics.py"]
