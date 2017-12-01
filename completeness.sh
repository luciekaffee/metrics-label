#!/usr/bin/env bash

FILE=$1
PROPERTIES=$2


grep -Fwf $PROPERTIES $FILE > labels.csv
echo "Created Labels File"
wc -l labels.csv

awk '{print $2"\n"$3}' $FILE | grep ^\<http | sort | uniq -u > objects.csv
echo "Created Properties and Objects File"
wc -l objects.csv

echo "Task 1"
echo "Completeness"

echo "Unique subjects"
awk '{print $1}' $FILE | sort | uniq -u | wc -l

echo "Number of unique entities with one or more labels"
awk '{print $1}' labels.csv | sort | uniq -u | wc -l



echo "Task 2"
echo "Efficient accessibility"

echo "Unique properties and objects"
wc -l objects.csv

echo "Number of unique properties and objects with one or more labels"
grep -Fwf objects.csv labels.csv | sort | uniq -u | wc -l

echo "Unambiguity"