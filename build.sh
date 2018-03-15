#!/bin/bash

. utils.sh

download_default_dict

mkdir -p security-anomalies-logs-data/input-data/
mkdir -p security-anomalies-logs-data/metrics/

docker build --rm -f Dockerfile-check -t tarkin-check:latest .
docker build --rm -f Dockerfile-check-demo -t tarkin-check-demo:latest .
docker build --rm -f Dockerfile-train -t tarkin-train:latest .
