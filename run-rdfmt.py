from Creator.CreatorRDFMT import *
import os
import json

basic = BasicRDFMTCreator()
cleaner = BasicRDFMTCleaner()
adder = RDFMTAdder()


print 'Basic start'
results = basic.run('../Metrics_Results')
print 'Cleaner start'
results = cleaner.run(results)
print 'Adder start'
results = adder.run(results)



