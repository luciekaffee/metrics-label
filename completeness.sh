#!/usr/bin/env bash

FILE=$1
PROPERTIES=$2
#LABELS="${3:-$PROPERTIES}"

awk '!seen[$0]++' $FILE > tmp && mv tmp $FILE
echo "Removed duplicate lines"

grep -Fwf $PROPERTIES $FILE > labels.csv
echo "Created Labels File"
wc -l labels.csv

awk '{print $1}' labels.csv | sort | uniq > has-labels.csv
echo "Created has-labels File"
wc -l has-labels.csv

awk '{print $2"\n"$3}' $FILE | grep e | sort | uniq > objects-properties.csv
# For Wikidata grep for www.wikidata.org/entity/
echo "Created Properties and Objects File"
wc -l objects-properties.csv

awk '{print $3}' $FILE | grep ^\<http | sort | uniq > objects.csv
echo "Created Properties and Objects File"
wc -l objects.csv

grep '\@' labels.csv | sed 's/.*\@//g' | awk '{$1=$1};1' | sort| uniq -c > languages.csv
echo "Created Languages File"
wc -l languages.csv

echo "Task 1"
echo "Completeness"

echo "Unique subjects"
awk '{print $1}' $FILE | sort | uniq | wc -l

echo "Number of unique entities with one or more labels"
awk '{print $1}' labels.csv | sort | uniq | wc -l

echo "Task 2"
echo "Efficient accessibility"

echo "Unique properties"
awk '{print $2}' data.nt | wc -l

echo "Number of unique properties and objects with one or more labels"
awk '{print $2}' data.nt | grep has-labels.csv | sort | uniq | wc -l
#grep -Fwf objects-properties.csv has-labels.csv | sort | uniq | wc -l


echo "Unique objects"
wc -l objects.csv

echo "Number of unique objects with one or more labels"
grep -Fwf objects.csv has-labels.csv | sort | uniq | wc -l

echo "Task 4"
echo "Multilinguality"

echo "Number of languages used"
wc -l languages.csv

echo "Number of labels in all languages"
cat languages.csv