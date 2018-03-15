#!/bin/bash

. utils.sh

LETTERSPACE_FILENAME=${2:-security-anomalies-logs-data/input-data/letterspace.pkl}
check_file_existence $LETTERSPACE_FILENAME

TMPDIRNAME=$(create_temp_dir)
cp $LETTERSPACE_FILENAME $TMPDIRNAME

time echo $1 | docker run -i -v $TMPDIRNAME:/tarkin/security-anomalies-logs-data/input-data/ tarkin-check-demo

rm -rf $TMPDIRNAME