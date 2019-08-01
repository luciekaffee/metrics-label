from Creator.CreatorRDFMT import *
import os
import json

merger = RDFMTMerger()
creator = BasicRDFMTCreator()
adder = RDFMTAdder()


print 'Merger start'
results = merger.run()
print 'Creator start'
results = creator.run(results)
print 'Adder start'
results = adder.run(results)



