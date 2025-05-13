FROM python:3.10.0

RUN mkdir -p /usr/backend/fastapi
WORKDIR /usr/backend/fastapi

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY rabbitmq_code /tmp/rabbitmq_code

RUN pip install /tmp/rabbitmq_code

COPY backend_fastAPI .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
