from python:3.5-slim

ENV VERSION=3.5
ENV ENV=test

RUN mkdir /app
WORKDIR /app

COPY .pipcache/3.5 /root/.cache/
COPY requirements-dev.txt /app/requirements.txt
RUN pip install -r requirements.txt

RUN python -m spacy download en

RUN rm -rf /root/.cache

COPY . /app
ENTRYPOINT ["/bin/bash"]