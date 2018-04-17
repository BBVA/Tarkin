from python:3.6.3-slim

ENV VERSION=3.6.3
ENV ENV=pro

RUN mkdir /app
WORKDIR /app

COPY .pipcache/3.6.3 /root/.cache/
COPY requirements.txt /app/requirements.txt
RUN pip install --no-index --find-links=/root/.cache/pip/w -r requirements.txt

RUN python -m spacy download en

RUN rm -rf /root/.cache

COPY . /app
ENTRYPOINT ["/bin/bash"]