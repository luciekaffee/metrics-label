#!/usr/bin/env bash

FILE=$1
PROPERTIES=$2
LANG=$3

echo "Task 3"
echo "Unambiguity"

grep -Fwf $LABELS $FILE > labels-only.csv
echo "Created Labels File"
wc -l labels-only.csv

echo "Number of entities that have more than one label with any property"
grep @$LANG labels-only.csv | awk '{print $1}' | sort | uniq -d | wc -l
# In case of no languages
#awk '{print $1}' labels-only.csv | sort | uniq -d | wc -l

echo "Number of entities that have more than one label with the same property"
grep @$LANG labels-only.csv | awk '{print $1 $2}' | sort | uniq -d | wc -l
# In case of no languages
#awk '{print $1 $2}' labels-only.csv | sort | uniq -d | wc -l