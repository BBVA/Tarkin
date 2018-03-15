#!/bin/bash

export PYTHONPATH=$(pwd)/security-anomalies-logs-data/

. utils.sh

CHECK_INPUT_FILE=${1:-security-anomalies-logs-data/data/input-logs-example-file.csv}
check_file_existence $CHECK_INPUT_FILE

mkdir -p security-anomalies-logs-data/input-data/
LETTERSPACE_FILENAME=${2:-security-anomalies-logs-data/input-data/letterspace.pkl}

rm $LETTERSPACE_FILENAME
time cat $CHECK_INPUT_FILE | python security-anomalies-logs-data/service/train.py
