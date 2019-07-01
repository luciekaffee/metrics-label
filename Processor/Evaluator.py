import json
import random
import copy
from sklearn.metrics import mean_squared_error
import operator
import numpy as np
from scipy.spatial import distance
from collections import Counter
from scipy.stats import kendalltau
from scipy.stats import spearmanr
from ranking_measures import measures
import math
from RBO import *

class CompareRankedLists:

    def __init__(self):
        self.rbo = RBO()
        self.kgs = ['wikidata', 'dbpedia', 'yago', 'linkedmdb', 'musicbrainz']

    def prepare_ranked_list(self, li):
        return [x[0].lower() for x in li]

    def prepare_ranked_list_ndcg(self, li):
        res = []
        di = dict((k.lower(), v) for k,v in dict(li).iteritems())
        for kg in self.kgs:
            res.append(di[kg])
        return res



    def run_kendalltau(self, gold_standard, ranked_lists):
        results = []
        for i in range(0, len(gold_standard)):
            result = {}
            for measure, li in ranked_lists.iteritems():
                gs = self.prepare_ranked_list(gold_standard[i])
                l = self.prepare_ranked_list(li[i])
                result[measure] = kendalltau(gs, l)
            results.append(result)
        return results

    def run_spearmanr(self, gold_standard, ranked_lists):
        results = []
        for i in range(0, len(gold_standard)):
            result = {}
            for measure, li in ranked_lists.iteritems():
                gs = self.prepare_ranked_list(gold_standard[i])
                l = self.prepare_ranked_list(li[i])
                result[measure] = spearmanr(gs, l)
            results.append(result)
        return results


    def run_RBO(self, gold_standard, ranked_lists):
        results = []
        for i in range(0, len(gold_standard)):
            result = {}
            for measure, li in ranked_lists.iteritems():
                gs = self.prepare_ranked_list(gold_standard[i])
                l = self.prepare_ranked_list(li[i])
                result[measure] = self.rbo.score(gs, l)
            results.append(result)
        return results

    # using ranking_measures from https://github.com/dkaterenchuk/ranking_measures
    def run_nDCG(self, gold_standard, ranked_lists):
        results = []
        for i in range(0, len(gold_standard)):
            result = {}
            for measure, li in ranked_lists.iteritems():
                #if measure == 'MSE':
                #    continue
                gs = self.prepare_ranked_list_ndcg(gold_standard[i])
                l = self.prepare_ranked_list_ndcg(li[i])
                result[measure] = measures.find_rankdcg(gs, l)
            results.append(result)
        return results