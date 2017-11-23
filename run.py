from processing.preprocessing_dumps import *
from processing.writer import *
from evaluators.property import *
from evaluators.evaluator import *

pre_btc_2010 = Preprocessing_BTC_2010( '../btc-2010/redirects.nx.gz', '../btc-2010/', 'data/1-btc-2010.csv')
label_properties = LabelingProperties()
writer = DictWriter()
completeness = CompletenessEvaluator()


pre_btc_2010.run()
properties = label_properties.run('data/1-btc-2010.csv')
properties =label_properties.limit(properties)
writer.write('data/properties.csv', properties)

### Evaluation ###

completeness.run('data/1-btc-2010.csv', 'data/properties.csv')

