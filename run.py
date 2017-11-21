from preprocessing.preprocessing_dumps import *
from evaluators.property import *

pre_btc_2010 = Preprocessing_BTC_2010('../btc-2010/', 'data/btc-2010.csv')
label_properties = LabelingProperties()


pre_btc_2010.run()
label_properties.run('data/btc-2010.csv')
