FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY app /app/app

# Seed DB on container start
CMD python -c "from app.seed import seed; seed()" &&     uvicorn app.main:app --host 0.0.0.0 --port 8000
