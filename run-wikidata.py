from Preprocessing.convertData import *
from Metrics.labelMetrics import *
from Metrics.labelingProperties import *

datafile = '../latest-truthy.nt.gz'
properties = 'Properties/properties-wikidata.csv'
languages = '../results/Languages/wikidata.csv'
monolanguages = '../results/Languages/wikidata-mono.csv'

completness = Completeness(datafile, properties, seperator=' ')
unam = Unambiguity(datafile, properties, seperator=' ')
langs = Multilinguality(datafile, languages, seperator=' ')
mono = MonolingualIsland(datafile, monolanguages, seperator=' ')
labusa = LabelAndUsage(datafile, 'out-wikidata-labelandusage.csv', properties, seperator=' ')

completness.run()
unam.run()
langs.run()
labusa.run()