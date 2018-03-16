#!/bin/bash

export PYTHONPATH=$(pwd)/Tarkin/

. utils.sh

CHECK_INPUT_FILE=${1:-Tarkin/data/input-logs-example-file.csv}
check_file_existence $CHECK_INPUT_FILE

mkdir -p Tarkin/input-data/
LETTERSPACE_FILENAME=${2:-Tarkin/input-data/letterspace.pkl}

rm $LETTERSPACE_FILENAME
time cat $CHECK_INPUT_FILE | python Tarkin/service/train.py
