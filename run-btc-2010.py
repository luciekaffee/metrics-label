from Preprocessing.convertData import *
from Metrics.labelMetrics import *

converter = ConvertData('out.csv', filename='btc-2010.csv')
completness = Completeness('out.csv', 'Properties/properties-btc2010.csv')
ea = EfficientAccessibility('out.csv', 'Properties/properties-btc2010.csv')

converter.run()
completness.run()
ea.run()