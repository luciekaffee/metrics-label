from Creator.CreatorRDFMT import *

basic = BasicRDFMTCreator()
cleaner = BasicRDFMTCleaner()

results = basic.run('../Metrics_Results')
cleaner.run(results)