#!/usr/bin/env bash

FILE=$1
SAMPLES=$2
PROPERTIES=$3

# For the Sampling
#for fn in data*
#do
#gunzip -cd $fn | head -100 >> samples.txt
#done

zgrep -f $PROPERTIES $FILE > labels.csv

cat labels.csv | awk '{print $1}' | sort | uniq > has-labels.csv

echo "NUMBER OF ENTITIES WITH LABELS"
awk '{print $1}' $SAMPLES | sort | uniq > sub.txt
grep -wf sub.txt has-labels.csv | wc -l
rm sub.txt

echo "NUMBER OF PROPERTIES WITH LABELS"
awk '{print $2}' $SAMPLES | sort | uniq > prop.txt
grep -wf prop.txt has-labels.csv | wc -l
rm prop.txt

echo "NUMBER OF OBJECTS WITH LABELS"
awk '{print $3}' $SAMPLES | grep ^\<http | sort | uniq > obj.txt
python2.7 find-nir.py
rm obj.txt

grep '\@' labels.csv | sed 's/.*\@//g' | awk '{$1=$1};1' | awk '{print $1}' | sort| uniq -c > languages.csv
echo "Created Languages File"


echo "UNAMBIGUITY"
grep @en labels.csv | awk '{print $1 $2}' | sort | uniq -d | wc -l
