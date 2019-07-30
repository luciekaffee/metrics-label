from Creator.CreatorRDFMT import *
from Creator.DataCollector import *
import os
import json

epp = EnpointPreparer()
bdc = BasicDataCollector()

endpoints = epp.run()
bdc.run(endpoints)

