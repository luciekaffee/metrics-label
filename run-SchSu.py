from Metrics.labelMetrics import *
from Metrics.labelingProperties import *

datafile = '../SchSu/data.nt'
properties = 'Properties/properties-schusu.csv'
languages = '../results/Languages/schusu.csv'
seperator = ' '

lpe = LabelingPropertiesExtractor(datafile, properties)
completness = Completeness(datafile, properties, seperator=seperator)
unam = Unambiguity(datafile, properties, seperator=seperator)
langs = Multilinguality(datafile, languages, seperator=seperator)

lpe.run()
completness.run()
unam.run()
langs.run()