#!/usr/bin/env bash

FILE=$1

awk '{print $2}' $FILE | sort | uniq -c