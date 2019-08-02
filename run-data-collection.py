from Creator.CreatorRDFMT import *
from Creator.DataCollector import *
import os
import json

#epp = EnpointPreparerBio2RDF()
epp = EnpointPreparerLSLOD()
bdc = BasicDataCollector()

endpoints = epp.run()
bdc.run(endpoints)

