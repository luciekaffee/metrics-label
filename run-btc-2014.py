from Preprocessing.convertData import *
from Metrics.labelMetrics import *
from Metrics.labelMetricsBTC import *
from Metrics.labelingProperties import *

datafile = 'btc-14.csv.gz'
properties = 'Properties/properties-btc2010.csv'
languages = '../results/Languages/btc14.csv'

converter = ConvertData(datafile, directory='../btc-2014/projects/btc-2014/data/crawls/')
completness = Completeness(datafile, properties, True)
#ea = EfficientAccessibility(datafile, properties, True)
unam = Unambiguity(datafile, properties, True) #23766617
labus = LabelAndUsage(datafile, 'labelus-btc14.csv', properties, True)
moreMetrics = BTC14()

converter.run_2014()
completness.run()
#ea.run()
unam.run()
labus.run()
moreMetrics.run()