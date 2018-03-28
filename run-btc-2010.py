from Preprocessing.convertData import *
from Metrics.labelMetrics import *

converter = ConvertData('out.csv', filename='btc-2010.csv')
completness = Completeness('out.csv', 'Properties/properties-btc2010.csv', True)
ea = EfficientAccessibility('out.csv', 'Properties/properties-btc2010.csv', True)
unam = Unambiguity('out.csv', 'Properties/properties-btc2010.csv', True)

converter.run()
completness.run()
ea.run()
unam.run()