from Processor.Ranker import *
import os
import json

rdfmts = {json.load(open('data/wikidata-rdfmt.json')), json.load(open('data/dbpedia-rdfmt.json')), json.load(open('data/yago-rdfmt.json')),
json.load(open('data/linkedmdb-rdfmt.json')), json.load(open('data/musicbrainz-rdfmt.json'))}

dc = DomainCreator()
acr = AnswerCompletenessRanker()
mtr = RDFMTRanker(rdfmts)

domains = dc.run(20, 5, language='en')

json.dump(domains, open('results/domains.json', 'w+'))

ranking_baseline = acr.run(domains)

json.dump(ranking_baseline, open('results/ranking-baselines.json', 'w+'))

mtr.run(domains)
