#Metrics Multilinguality on the Semantic Web

This repository contains a set of scripts to analyze different N-Triple datasets in order to measure their converage of labels and multilinguality.

All dumps, that are in the nt format and do only contain triples, can be processed right away.

We tested the scripts on the following datasets:

- Swiss National Library Bibliographische Daten
- British Bibliographic Data
- Taiwan Open Data: Public Services
- British Open Data: Schools in Surrey

In order to process BTC 2010, the python script preprocess-BTC.py is needed.

After preprocessing or simply unzipping the datasets, a file with labeling properties is needed.

We used properties.sh to see a listing of properties and their usage in a dump and select manually the ones that are used for labeling.

Properties identified as labeling properties can be found in the **properties** folder. The second version of each properties file identifies the labeling properties, excluding properties for e.g. description or alternative titles. 

Finally completeness.sh can be run.
This script takes two arguments: The dataset file, and the labeling properties file.

The second script for the analyzes is unambiguity.sh. 
This script takes three arguments: The dataset file, and the labeling properties file. In our case we use the labeling properties in the second properties file. The third argument is a language code as it would appear in the dataset.

NIR.sh count the number of objects that are non-information resources to get an overview on how many (non) information resources a dataset provides.

_Hint_:
As Wikidata's/BTC database dump is quite large, while the completness.sh script should work in theory, it would take large amounts of memory.
Therefore, Wikidata can be analyzed with the wikidata.sh script, and from there can use parts of the completness.sh script, depending on memory capabilities.
