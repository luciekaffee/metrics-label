from Creator.CreatorRDFMT import *
import os
import json

basic = BasicRDFMTCreator()
cleaner = BasicRDFMTCleaner()
adder = RDFMTAdder()



results = basic.run('../Metrics_Results')
results = cleaner.run(results)
results = adder.run(results)



