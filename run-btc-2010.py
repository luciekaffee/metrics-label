from Preprocessing.convertData import *
from Metrics.labelMetrics import *

converter = ConvertData('out.csv', directory='../btc-2010')
completness = Completeness('out.csv', 'Properties/properties-btc2010.csv')

converter.run_compressed()
completness.run()
