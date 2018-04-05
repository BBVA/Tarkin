#!/bin/bash

. utils.sh

LETTERSPACE_FILENAME=${2:-input-data/letterspace.pkl}
check_file_existence $LETTERSPACE_FILENAME

TMPDIRNAME=$(create_temp_dir)
cp $LETTERSPACE_FILENAME $TMPDIRNAME

time echo $1 | docker run -i -v $TMPDIRNAME:/tarkin/input-data -v $(pwd)/data/vocab:/tarkin/data/vocab -v $(pwd)/metrics:/tarkin/metrics tarkin-check-demo

rm -rf $TMPDIRNAME