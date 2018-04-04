#!/bin/bash

export PYTHONPATH="$(pwd)/../../:$(pwd)/src/"

. utils.sh

CHECK_INPUT_FILE=${1:-data/input-logs-example-file.csv}
check_file_existence $CHECK_INPUT_FILE

mkdir -p input-data/
LETTERSPACE_FILENAME=${2:-input-data/letterspace.pkl}

rm $LETTERSPACE_FILENAME
time cat $CHECK_INPUT_FILE | python src/train.py
