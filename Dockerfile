FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir fastapi uvicorn

CMD ["uvicorn", "autogo_erp.main:app", "--host", "0.0.0.0", "--port", "8000"]

