from Processor.Ranker import *
from Processor.Evaluator import *
from Processor.DomainCreator import *
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

dc = RandomDomainCreator(['en', 'es', 'hi'])
ds = DomainSelector(['en', 'es', 'hi'])
br = BaselineRanker()
mtr = RDFMTRanker(rdfmts)
gr = GoldStandardRanker(gold_en, gold_es, gold_hi)

cl = CompareRankedLists()

#domains = dc.run(288, 1, language='es', domains='Film')
domains = dc.run(20, 5)
#domain = 'Music'
#domains = ds.run(domain)

#json.dump(domains, open('results/domains.json', 'w+'))

ranking_baseline_noCLC = br.run_NoCLC(domains)
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


ranked_lists = {'NoCLC': ranking_baseline_noCLC, 'MSE': ranking_baseline_mse, 'Cos': ranking_baseline_cos, 'CosN': ranking_baseline_cos_num, 'rdfmt': rdfmt_eval}
#print 'gold standard: ' + str(ranking_gold_standard)
#print 'NoCLC:' + str(ranking_baseline_noCLC) + '\nMSE: ' + str(ranking_baseline_mse) + '\nCos: ' + str(ranking_baseline_cos) + '\nCosN: ' + str(ranking_baseline_cos_num) + '\nrdfmt: ' + str(rdfmt_eval)

kt = cl.run_kendalltau(ranking_gold_standard, ranked_lists)
sr = cl.run_spearmanr(ranking_gold_standard, ranked_lists)
rbo = cl.run_RBO(ranking_gold_standard, ranked_lists)
ndcg = cl.run_nDCG(ranking_gold_standard, ranked_lists)

print 'Kendall Tau: ' + str(kt)
print 'Spearman Rho: '+ str(sr)
print 'Rank Biased Overlap: ' + str(rbo)
print 'Normalized Discounted Cumulative Gain: ' + str(ndcg)

results = {'domains': domains, 'ranked_lists': {'Gold_Standard': ranking_gold_standard, 'NoCLC': ranking_baseline_noCLC, 'MSE': ranking_baseline_mse, 'Cos': ranking_baseline_cos, 'CosN': ranking_baseline_cos_num, 'CLC': rdfmt_eval}, 'metrics_results': {'kendalltau':kt, 'spearmanrho':sr, 'rankedbiasoverlap':rbo, 'ndcg':ndcg}}

json.dump(results, open('results/experiment-results-multi.json', 'wb'))
#json.dump(results, open('results/domains/experiment-results-' + domain + '.json', 'wb'))