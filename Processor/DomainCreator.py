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
import itertools


class RandomDomainCreator:

    def __init__(self, languages):
        self.query_ids = json.load(open('data/query-ids.json'))
        self.classes = json.load(open('data/classes.json'))
        self.languages = languages


    def get_qids_from_classes(self, kg, lang):
        qids = []
        for key, classes in self.classes[kg].iteritems():
            if classes:
                qids.append(key)
        return qids

    def get_queries_all(self, number_queries, lang):
        result = {}
        qids = copy.copy(self.query_ids)
        random.shuffle(qids)
        for q in qids[:number_queries]:
            if lang:
                result[q] = lang
            else:
                result[q] = random.choice(self.languages)
        return result


    def get_queries_selected(self, qids, number_queries, lang):
        result = {}
        if number_queries > len(qids):
            number_queries = len(qids)
        random.shuffle(qids)
        for q in qids[:number_queries]:
            if lang:
                result[q] = lang
            else:
                result[q] = random.choice(self.languages)
        return result

    # Options for domains: Music, Film
    # Language options are either en, hi, es or None, so it will pick a language for each query at random
    def run(self, number_queries, number_sets, domains=None, language=None):
        queries_result = []

        if not domains:
            for x in range(0, number_sets):
                queries_result.append(self.get_queries_all(number_queries, language))

        elif domains == 'Music':
            qids = self.get_qids_from_classes('MusicBrainz', language)
            for x in range(0, number_sets):
                queries_result.append(self.get_queries_selected(qids, number_queries, language))

        elif domains == 'Film':
            qids = self.get_qids_from_classes('linkedmdb', language)
            for x in range(0, number_sets):
                queries_result.append(self.get_queries_selected(qids, number_queries, language))

        else:
            print 'Please add a valid domain, either "Music" or "Film"'

        return queries_result

class DomainSelector:

    def __init__(self, languages):
        self.domains = json.load(open('data/domains/domains.json'))
        self.classes = json.load(open('data/classes.json'))
        self.languages = languages

    def run(self, domain, language=None):
        queries_result = {}
        if not domain in self.domains:
            print 'select one of the following domains: ' + str(self.domains.keys())
            return
        for qid in self.domains[domain]:
            if language:
                queries_result[qid] = language
            else:
                queries_result[qid] = random.choice(self.languages)
        return [queries_result]

