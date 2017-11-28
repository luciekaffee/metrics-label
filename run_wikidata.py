from processing.preprocessing_dumps import *
from processing.writer import *
from evaluators.property import *
from evaluators.evaluator import *

pre_wd = Preprocessing_Wikidata('../wikidata/latest-truthy.nt.gz', 'data/wikidata.csv')
label_properties = LabelingProperties()
writer = DictWriter()
LC = CompletenessEvaluator()


# @todo: writer for the entities, similar to properties too!
pre_wd.run()
print "Created dump file"
properties = label_properties.run('data/wikidata.csv')
properties =label_properties.limit(properties)
writer.write('data/wd-properties.csv', properties)
print "Processed labeling properties"

### Evaluation ###

print LC.run('data/wikidata.csv', 'data/wd-properties.csv')