#!/bin/bash

export PYTHONPATH="$(pwd)/../../:$(pwd)/src/"

. utils.sh

CHECK_INPUT_FILE=${1:-data/input-logs-example-file.csv}
check_file_existence $CHECK_INPUT_FILE

mkdir -p freq-data/
export LETTERSPACE_FILENAME=${2:-freq-data/letterspace.pkl}

rm $LETTERSPACE_FILENAME
time cat $CHECK_INPUT_FILE | python src/train.py
