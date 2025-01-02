FROM python:3.9-slim

RUN adduser --disabled-password appuser
WORKDIR /app
COPY --chown=appuser:appuser . .

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

USER appuser

EXPOSE 8000
EXPOSE 5432

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
