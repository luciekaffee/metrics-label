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
This script takes two arguments: The dataset file, and the labeling properties file.