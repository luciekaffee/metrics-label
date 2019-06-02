from Creator.CreatorRDFMT import *
import os
import json

basic = BasicRDFMTCreator()
cleaner = BasicRDFMTCleaner()
adder = RDFMTAdder()



#results = basic.run('../Metrics_Results')
#results = cleaner.run(results)
#results = adder.run(results)

# this function replaces the above the calls to run of the classes.
# mainly to be lazy and safe us from running the whole pipeline when testing
def get_existing_RDFMT_files():
    results = {}

    for filename in os.listdir('data'):
        if filename.endswith('-rdfmt.json'):
            with open(filename) as infile:
                data = json.load(infile)
                results[filename.replace('-rdfmt.json', '')] = data
    return results

results = get_existing_RDFMT_files()

all_query_results = {}

with open('all-query-results.json') as infile:
    all_query_results = json.load(infile)


