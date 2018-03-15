#!/bin/bash

. utils.sh

CHECK_INPUT_FILE=${1:-security-anomalies-logs-data/data/input-logs-example-file.csv}
check_file_existence $CHECK_INPUT_FILE

LETTERSPACE_FILENAME=${2:-security-anomalies-logs-data/input-data/letterspace.pkl}

TMPDIRNAME=$(create_temp_dir)

time cat $CHECK_INPUT_FILE | docker run -i -v $TMPDIRNAME:/tarkin/security-anomalies-logs-data/input-data tarkin-train

mv $TMPDIRNAME/letterspace.pkl $LETTERSPACE_FILENAME

rm -rf $TMPDIRNAME
