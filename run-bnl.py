from Metrics.labelMetrics import *
from Metrics.labelingProperties import *

datafile = '../BNL/bnl.nt'
properties = 'Properties/properties-bnl.csv'
seperator = ' '

#lpe = LabelingPropertiesExtractor(datafile, properties)
completness = Completeness(datafile, properties, seperator=seperator)
unam = Unambiguity(datafile, properties, seperator=seperator)

#lpe.run()
completness.run()
unam.run()