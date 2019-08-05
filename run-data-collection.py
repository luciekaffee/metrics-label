from Creator.CreatorRDFMT import *
from Creator.DataCollector import *
import os
import json

#epp = EnpointPreparerBio2RDF()
#epp = EnpointPreparerLSLOD()
bdc = BasicDataCollector()

#endpoints = epp.run()
endpoints = {'DBpedia': 'http://node1.research.tib.eu:4001/sparql'}
bdc.run(endpoints, json.load(open('data/classes-dbpedia.json')))

