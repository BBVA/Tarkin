FROM python:3.6.3-slim as tarkin_build
RUN mkdir /tarkin
WORKDIR /tarkin

RUN apt-get update && apt-get install -y build-essential
COPY requirements.txt /tarkin/requirements.txt
COPY setup.py /tarkin/setup.py

RUN pip install -r /tarkin/requirements.txt
RUN pip install wheel

FROM python:3.6.3-slim

COPY Tarkin /tarkin/Tarkin
COPY setup.py /tarkin/setup.py

COPY --from=tarkin_build /tarkin /tarkin
COPY --from=tarkin_build /root/.cache /root/.cache
WORKDIR /tarkin
COPY requirements.txt /tarkin/requirements.txt
RUN pip install -r /tarkin/requirements.txt
RUN python -m spacy download en

RUN rm -rf /root/.cache

ENV PYTHONPATH=Tarkin/
ENTRYPOINT python Tarkin/service/check.py
