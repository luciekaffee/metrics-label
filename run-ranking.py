from Processor.Ranker import *
import os
import json

wd_rdfmt = json.load(open('data/wikidata-rdfmt.json'))
dbpedia_rdfmt = json.load(open('data/dbpedia-rdfmt.json'))
yago_rdfmt = json.load(open('data/yago-rdfmt.json'))
linked_rdfmt = json.load(open('data/linkedmdb-rdfmt.json'))
mb_rdfmt = json.load(open('data/musicbrainz-rdfmt.json'))
rdfmts = {}
rdfmts.update(wd_rdfmt)
rdfmts.update(dbpedia_rdfmt)
rdfmts.update(yago_rdfmt)
rdfmts.update(linked_rdfmt)
rdfmts.update(mb_rdfmt)

dc = DomainCreator(['en', 'es', 'hi'])
acr = AnswerCompletenessRanker()
mtr = RDFMTRanker(rdfmts)

#domains = dc.run(288, 1, language='en')
domains = dc.run(288, 1)

json.dump(domains, open('results/domains.json', 'w+'))

ranking_baseline = acr.run(domains)

#json.dump(ranking_baseline, open('results/ranking-baselines.json', 'w+'))

rdfmt_eval = mtr.run(domains)

print ranking_baseline
print rdfmt_eval
