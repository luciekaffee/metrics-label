from Processor.Ranker import *
from ranking_measures import measures
import os
import json

wd_rdfmt = json.load(open('data/rdfmt/wikidata-rdfmt.json'))
dbpedia_rdfmt = json.load(open('data/rdfmt/dbpedia-rdfmt.json'))
yago_rdfmt = json.load(open('data/rdfmt/yago-rdfmt.json'))
linked_rdfmt = json.load(open('data/rdfmt/linkedmdb-rdfmt.json'))
mb_rdfmt = json.load(open('data/rdfmt/musicbrainz-rdfmt.json'))
rdfmts = {}
rdfmts.update(wd_rdfmt)
rdfmts.update(dbpedia_rdfmt)
rdfmts.update(yago_rdfmt)
rdfmts.update(linked_rdfmt)
rdfmts.update(mb_rdfmt)

gold_en = json.load(open('data/goldstandard/gold-standard-en.json'))
gold_es = json.load(open('data/goldstandard/gold-standard-es.json'))
gold_hi = json.load(open('data/goldstandard/gold-standard-hi.json'))

dc = DomainCreator(['en', 'es', 'hi'])
br = BaselineRanker()
mtr = RDFMTRanker(rdfmts)
gr = GoldStandardRanker(gold_en, gold_es, gold_hi)

cl = CompareRankedLists()

#domains = dc.run(288, 1, language='en', domains='Film')
domains = dc.run(288, 1, language='hi')

#json.dump(domains, open('results/domains.json', 'w+'))

ranking_baseline_mse = br.run_mse(domains)
ranking_baseline_cos = br.run_cos(domains)
ranking_baseline_cos_num = br.run_cos_numbers(domains)

#json.dump(ranking_baseline, open('results/ranking-baselines.json', 'w+'))

rdfmt_eval = mtr.run(domains)
#print rdfmt_eval

ranking_gold_standard = gr.run(domains)

#print 'MSE\n' + str(ranking_baseline_mse)
#print 'Cos, binary\n' + str(ranking_baseline_cos)
#print 'Cos, numbers\n' + str(ranking_baseline_cos_num)
#print rdfmt_eval

#print 'Gold standard\n' + str(ranking_gold_standard)


ranked_lists = {'MSE': ranking_baseline_mse, 'Cos': ranking_baseline_cos, 'CosN': ranking_baseline_cos_num, 'rdfmt': rdfmt_eval}
print 'gold standard: ' + str(ranking_gold_standard)
print 'MSE: ' + str(ranking_baseline_mse) + '\nCos: ' + str(ranking_baseline_cos) + '\nCosN: ' + str(ranking_baseline_cos_num) + '\nrdfmt: ' + str(rdfmt_eval)

print 'Kendall Tau: ' + str(cl.run_kendalltau(ranking_gold_standard, ranked_lists))
print 'Spearman Rho: '+ str(cl.run_spearmanr(ranking_gold_standard, ranked_lists))
print 'Rank Biased Overlap: ' + str(cl.run_RBO(ranking_gold_standard, ranked_lists))
print 'Normalized Discounted Cumulative Gain: ' + str(cl.run_nDCG(ranking_gold_standard, ranked_lists))

results = {'ranked_lists': {'MSE': ranking_baseline_mse, 'Cos': ranking_baseline_cos, 'CosN': ranking_baseline_cos_num, 'rdfmt': rdfmt_eval}, 'metrics_results': {'kendalltau':cl.run_kendalltau(ranking_gold_standard, ranked_lists), 'spearmanrho':cl.run_spearmanr(ranking_gold_standard, ranked_lists), 'rankedbiasoverlap':cl.run_RBO(ranking_gold_standard, ranked_lists), 'ndcg':cl.run_nDCG(ranking_gold_standard, ranked_lists)}}

json.dumps(results, 'results/experiment-results.json')