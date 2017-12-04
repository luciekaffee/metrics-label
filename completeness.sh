#!/usr/bin/env bash

FILE=$1
PROPERTIES=$2


awk '!seen[$0]++' $FILE > tmp && mv tmp $FILE
echo "Removed duplicate lines"

grep -Fwf $PROPERTIES $FILE > labels.csv
echo "Created Labels File"
wc -l labels.csv

awk '{print $1}' labels.csv > has-labels.csv
echo "Created has-labels File"
wc -l has-labels.csv

awk '{print $2"\n"$3}' $FILE | grep ^\<http | sort | uniq > objects.csv
echo "Created Properties and Objects File"
wc -l objects.csv

echo "Task 1"
echo "Completeness"

echo "Unique subjects"
awk '{print $1}' $FILE | sort | uniq | wc -l

echo "Number of unique entities with one or more labels"
awk '{print $1}' labels.csv | sort | uniq | wc -l

echo "Task 2"
echo "Efficient accessibility"

echo "Unique properties and objects"
wc -l objects.csv

echo "Number of unique properties and objects with one or more labels"
grep -Fwf objects.csv has-labels.csv | sort | uniq | wc -l

echo "Task 3"
echo "Unambiguity"

echo "Number of entities that have more than one label with any property"
awk '{print $1}' labels.csv | sort | uniq -d | wc -l

echo "Number of entities that have more than one label with the same property"
awk '{print $1 $2}' labels.csv | sort | uniq -d | wc -l