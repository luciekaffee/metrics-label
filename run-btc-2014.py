from Preprocessing.convertData import *
from Metrics.labelMetrics import *
from Metrics.labelingProperties import *

datafile = 'btc-14.csv'
properties = 'Properties/properties-btc2010.csv'
languages = '../results/Languages/schusu.csv'

converter = ConvertData(datafile, directory='../btc-2014/projects/btc-2014/data/crawls/')
completness = Completeness(datafile, properties, True)
#ea = EfficientAccessibility(datafile, properties, True)
unam = Unambiguity(datafile, properties, True)

converter.run_2014()
completness.run()
#ea.run()
unam.run()