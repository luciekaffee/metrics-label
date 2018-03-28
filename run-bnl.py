from Metrics.labelMetrics import *

datafile = '../BNL/bnl.nt'
properties = 'Properties/properties-bnl.csv'

completness = Completeness(datafile, properties)
ea = EfficientAccessibility(datafile, properties)
unam = Unambiguity(datafile, properties)

converter.run()
completness.run()
ea.run()
unam.run()