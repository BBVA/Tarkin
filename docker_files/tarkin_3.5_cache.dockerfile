from python:3.5-slim

RUN mkdir /app
WORKDIR /app

RUN apt-get update && apt-get install -y build-essential
COPY .pipcache/3.5/pip /root/.cache/pip


COPY requirements.txt /app/requirements.txt
RUN pip wheel --wheel-dir=/root/.cache/pip/w -r requirements.txt && rm /app/requirements.txt

COPY requirements-dev.txt /app/requirements.txt
RUN pip wheel --wheel-dir=/root/.cache/pip/w -r requirements.txt && rm /app/requirements.txt


RUN chmod -R 777 /root/.cache