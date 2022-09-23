FROM python:3.9.14

COPY ./requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

ENTRYPOINT python /app/app.py