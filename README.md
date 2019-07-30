# Metrics Labels

This code is the base to create RDF Molecule Templates and compare knowledge graphs based on their labeling and multilinguality.

## Create RDF MT (Creator)

The *Creator* module creates the RDF MT template based on the results of the queries in *Queries.pfd* written to a single file each. Careful! The queries for Wikidata need *a* (rdf:type) to be replaced by *wdt:P31* (Wikidata's instance of).
*\<RDFMT1\>* or *\<%s\>* need to be replaced with the respective classes of the knowledge graph, i.e., the queries will be executed once for each class.

The creation can be run using **run-rdfmt.py**, which writes the RDFMT files as json files to the *data/rdfmt/* folder.

## Graphs

The *graphs* folder contains a jupyter notebook to create figures and analyze the RDFMTs overall.
