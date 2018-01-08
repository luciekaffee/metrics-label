#!/usr/bin/env bash

FILE=$1

awk '{print $3}' $FILE | grep '^<http' | sed 's/<//g' | sed 's/>//g' | sort | uniq | while read url; do curl -I $url; done | grep -E '303|302' |wc -l