#!/bin/bash

. utils.sh

mkdir -p Tarkin/data/vocab/
download_default_dict

mkdir -p Tarkin/input-data/
mkdir -p Tarkin/metrics/

docker build --rm -f Dockerfile-check -t tarkin-check:latest .
docker build --rm -f Dockerfile-check-demo -t tarkin-check-demo:latest .
docker build --rm -f Dockerfile-train -t tarkin-train:latest .
