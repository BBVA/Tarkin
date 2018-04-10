#!/bin/bash

. utils.sh

pushd ../../
python setup.py sdist
popd

mkdir -p data/vocab/
download_default_dict

mkdir -p freq-data/
mkdir -p metrics/

cp -r ../../dist .

docker build --rm -f docker/Dockerfile-check -t tarkin-check:latest .
docker build --rm -f docker/Dockerfile-check-demo -t tarkin-check-demo:latest .
docker build --rm -f docker/Dockerfile-train -t tarkin-train:latest .
