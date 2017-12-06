#!/usr/bin/env bash

FILE=$1

grep '".*"' $FILE | awk '{print $2}' | sort | uniq -c