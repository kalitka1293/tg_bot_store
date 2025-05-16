FROM python:3.10.0

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/usr/backend/django/website_store
ENV DJANGO_SETTINGS_MODULE=website_store.settings

RUN mkdir -p /usr/backend/django 
WORKDIR /usr/backend/django

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY rabbitmq_code /tmp/rabbitmq_code

RUN pip install /tmp/rabbitmq_code

COPY website_store ./website_store

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "120", "--access-logfile", "-", "website_store.wsgi"]


