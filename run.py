from Creator.CreatorRDFMT import *

basic = BasicRDFMTCreator()
cleaner = BasicRDFMTCleaner()
adder = RDFMTAdder()

results = basic.run('../Metrics_Results')
results = cleaner.run(results)
adder.run(results)
