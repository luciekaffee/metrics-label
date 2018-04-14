from Metrics.labelMetrics import *
from Metrics.labelingProperties import *

datafile = '../taips/data.nt'
properties = 'Properties/properties-taips.csv'
properties_unam = 'Properties/properties-taips-2.csv'
languages = '../results/Languages/taips.csv'
seperator = ' '

#lpe = LabelingPropertiesExtractor(datafile, properties)
completness = Completeness(datafile, properties, seperator=seperator)
unam = Unambiguity(datafile, properties_unam, seperator=seperator)
langs = Multilinguality(datafile, languages, seperator=seperator)
mono = MonolingualIsland(datafile, '../results/Languages/taips-mono.csv', seperator=seperator)
labus = LabelAndUsage(datafile, '../results/taips-usage.csv', properties, seperator=seperator)

#lpe.run()
completness.run()
unam.run()
langs.run()
mono.run()
labus.run()