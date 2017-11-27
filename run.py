from processing.preprocessing_dumps import *
from processing.writer import *
from evaluators.property import *
from evaluators.evaluator import *

pre_btc_2010 = Preprocessing_BTC_2010('../btc-2010/', 'data/1-btc-2010.csv')
label_properties = LabelingProperties()
writer = DictWriter()
LC = CompletenessEvaluator()


# @todo: writer for the entities, similar to properties too!
#pre_btc_2010.run()
pre_btc_2010.limit('../btc-2010/redirects.nx.gz', 'data/1-nir-btc-2010.csv')
writer.writeEntities()
properties = label_properties.run('data/1-nir-btc-2010.csv')
properties =label_properties.limit(properties)
writer.write('data/2-properties.csv', properties)

### Evaluation ###

print LC.run('data/1-nir-btc-2010.csv', 'data/2-properties.csv')
