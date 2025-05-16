FROM python:3.10

RUN mkdir -p /usr/backend/service_meilisearch
WORKDIR /usr/backend/service_meilisearch

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY  /tg_bot_store/library/rabbitmq_code /tmp/rabbitmq_code

RUN pip install /tmp/rabbitmq_code

COPY meilisearch_store .

CMD [ "python", "main.py" ]

