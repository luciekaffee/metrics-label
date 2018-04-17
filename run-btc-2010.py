from Preprocessing.convertData import *
from Metrics.labelMetrics import *
from Metrics.labelingProperties import *
from Metrics.labelMetricsBTC import *

converter = ConvertData('out.csv', directory='../btc-10/')
completness = Completeness('out.csv', 'Properties/properties-btc2010.csv', True)
ea = EfficientAccessibility('out.csv', 'Properties/properties-btc2010.csv', True)
unam = Unambiguity('out.csv', 'Properties/properties-btc2010.csv', True)
labus = LabelAndUsage('out.csv', 'labelus-btc10.csv', 'Properties/properties-btc2010.csv', True)
more = BTC10('../btc-2010/', 'monoling-btc-10.csv')

converter.run_compressed()
completness.run()
ea.run()
unam.run()
labus.run()
more.run()


