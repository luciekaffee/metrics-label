from Preprocessing.convertData import *
from Metrics.labelMetrics import *
from Metrics.labelingProperties import *

datafile = '../latest-truthy.nt.gz'
datasmall = 'latest-truthy-small.nt.gz'
properties = 'Properties/properties-wikidata.csv'
languages = '../results/Languages/wikidata.csv'
monolanguages = '../results/Languages/wikidata-mono.csv'

convert = ConvertDataWikidata(datafile, datasmall)
convert.run()

completness = Completeness(datasmall, properties)
unam = Unambiguity(datasmall, properties)
langs = Multilinguality(datasmall, languages)
mono = MonolingualIsland(datasmall, monolanguages)
labusa = LabelAndUsage(datasmall, 'out-wikidata-labelandusage.csv', properties)

completness.run()
unam.run()
langs.run()
labusa.run()