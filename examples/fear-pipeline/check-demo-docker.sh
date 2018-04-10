#!/bin/bash

. utils.sh

LETTERSPACE_FILENAME=${2:-freq-data/letterspace.pkl}
check_file_existence $LETTERSPACE_FILENAME

TMPDIRNAME=$(create_temp_dir)
cp $LETTERSPACE_FILENAME $TMPDIRNAME

time echo $1 | docker run -i -e LETTERSPACE_FILENAME=freq-data/letterspace.pkl -v $TMPDIRNAME:/tarkin/freq-data -v $(pwd)/data/vocab:/tarkin/data/vocab -v $(pwd)/metrics:/tarkin/metrics tarkin-check-demo

rm -rf $TMPDIRNAME