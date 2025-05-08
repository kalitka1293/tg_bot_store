FROM python:3.10.0

RUN mkdir -p /usr/backend/django 
WORKDIR /usr/backend/django

COPY website_store/requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY library/rabbitmq_code /tmp/rabbitmq_code

RUN pip install /tmp/rabbitmq_code

COPY website_store .

EXPOSE 8080

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]


