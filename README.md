#Metrics Multilinguality on the Semantic Web

This repository contains a set of scripts to analyze different N-Triple datasets in order to measure their converage of labels and multilinguality.

All dumps, that are in the nt format and do only contain triples, can be processed right away.

We tested the script(s) on the following datasets:

- Wikidata
- BTC 2010 and BTC 2014
- Swiss National Library Bibliographische Daten

In order to process BTC 2010, the python script preprocess-BTC-2010.py is needed.

After preprocessing or simply unzipping the datasets, a file with labeling properties is needed.

We used properties.sh to see a listing of properties and their usage in a dump and select manually the ones that are used for labeling.

Finally completeness.sh can be run.
This script takes two or three arguments: The dataset file, and the labeling properties file.
Aditionally, if unambiguity should run with a different subset of properties those can be passed as the third argument.

Hint:
As Wikidata's database dump is quite large and we can assume that the data is not as noisy as our other datasets, it is recommend 
for performance reasons to comment the removal of multiple lines in the beginning of the bash script.