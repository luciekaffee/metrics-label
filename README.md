# Metrics Labels

This code is the base to create RDF Molecule Templates and compare knowledge graphs based on their labeling and multilinguality.

The *Creator* module creates the RDF MT template based on the results of the queries in *Queries.pfd* written to a single file each. Careful! The queries for Wikidata need *a* (rdf:type) to be replaced by *wdt:P31* (Wikidata's instance of).
*\<RDFMT1\>* needs to be replaced with the respective classes of the knowledge graph, i.e., the queries will be executed once for each class.

The file *data/all-query-results.json* contains the answer for the list of queries based on QALD. 

The *Processor* module can be run independently of the Creator or in a pipeline right after. It reads from the files created previously in the *data* folder.
The class *RDFMT_all_data.py* creates statistics across all RDF MTs. 
The class *ranker.py* creates a ranking of the datasets based on the queries of *all-query-results.json* and the RDF MT modules, compared with just the results from the queries.
