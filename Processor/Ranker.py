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



class DomainCreator:

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

class BaselineRanker:

    def __init__(self):
        self.answers = json.load(open('data/all-query-results.json'))
        self.kgs = ['Wikidata', 'DBpedia', 'YAGO', 'LinkedMDB', 'MusicBrainz']
        self.query_ids = json.load(open('data/query-ids.json'))
        self.answers_numbers = self.get_answer_numbers()

    def get_answer_numbers(self):
        result = {}
        data = json.load(open('data/qald-9-train-multilingual.json'))
        for q in data['questions']:
            if int(q['id']) not in self.query_ids:
                continue
            result[q['id']] = len(q['answers'][0]['results']['bindings'])
        return result

    # NOT USED, based on https://rem.jrc.ec.europa.eu/RemWeb/atmes2/20b.htm
    def calculate_nmse(self, gold, data):
        counter = 0
        p_num = sum(gold)/len(gold)
        m_num = sum(data)/len(gold)
        num = p_num * m_num
        for x in range(0, len(gold)):
            c = math.pow(gold[x] - data[x], 2)
            c = c / num
            counter += c
        return counter / num 

    # NOT USED, based on https://gist.github.com/amanahuja/6315882
    def mean_absolute_percentage_error(self, y_true, y_pred): 
        y_true, y_pred = np.array(y_true), np.array(y_pred)
        return np.mean(np.abs((y_true - y_pred) / y_true))

    def normalize_mse(self, data):
        result = {}
        arr = []
        for k,v in data.iteritems():
            arr.append(v)
        maxi = max(arr)
        for k,v in data.iteritems():
            result[k] = 1 - (v/maxi)
        return result


    def get_errors(self, qid_set):
        kg_answers = {}
        gold_answers = []
        for qid, lang in qid_set.iteritems():
            gold_answers.append(self.answers_numbers[str(qid)])
        for kg in self.kgs:
            kg_answers[kg] = []
            for qid, lang in qid_set.iteritems():
                if not str(qid) in self.answers[lang][kg]:
                    kg_answer = 0
                else:
                    kg_answer = len(self.answers[lang][kg][str(qid)])
                #if kg_answer == 0:

                kg_answers[kg].append(kg_answer)
        errors = {}
        for kg, e in kg_answers.iteritems():
            errors[kg] = mean_squared_error(gold_answers, e)
        errors = self.normalize_mse(errors)
        return errors

    def get_cos(self, qid_set):
        kg_answers = {}
        ideal = [1] * len(qid_set)
        for kg in self.kgs:
            kg_answers[kg] = []
            for qid, lang in qid_set.iteritems():
                if not str(qid) in self.answers[lang][kg]:
                    kg_answers[kg].append(0)
                elif not self.answers[lang][kg][str(qid)]:
                    kg_answers[kg].append(0)
                else:
                    kg_answers[kg].append(1)
        similarity = {}
        for kg, vec in kg_answers.iteritems():
            if all(v == 0 for v in vec):
                similarity[kg] = 0
                continue
            similarity[kg] = distance.cosine(ideal, vec)
        return similarity

    def get_cos_numbers(self, qid_set):
        kg_answers = {}
        gold_answers = []

        for qid, lang in qid_set.iteritems():
            gold_answers.append(self.answers_numbers[str(qid)])

        for kg in self.kgs:
            kg_answers[kg] = []
            for qid, lang in qid_set.iteritems():
                if not str(qid) in self.answers[lang][kg]:
                    kg_answers[kg].append(0)
                elif not self.answers[lang][kg][str(qid)]:
                    kg_answers[kg].append(0)
                else:
                    kg_answers[kg].append(1)
        similarity = {}
        for kg, vec in kg_answers.iteritems():
            if all(v == 0 for v in vec):
                similarity[kg] = 0
                continue
            similarity[kg] = 1 - distance.cosine(gold_answers, vec)
        return similarity

    def normalize_NoCLC(self, metric, baseline_data):
        maxi = []
        result = {}
        for kg, data in baseline_data.iteritems():
            maxi.append(data[metric])
        for kg, data in baseline_data.iteritems():
            result[kg] = {}
            for k,v in data.iteritems():
                if k == metric:
                    result[kg][k] = v/max(maxi)
                else:
                    result[kg][k] = v
        return result


    def get_NoCLC(self, qid_set):
        kg_answers = {}
        baseline_data = json.load(open('data/baselines/baseline_kgs_metrics.json'))
        languages = dict([(k, len(list(v))) for k, v in itertools.groupby(sorted(qid_set.values()))])
        for kg, data in baseline_data.iteritems():
            langs = data['languages_share'] 
            if len(languages) ==  1 and languages.keys()[0] in langs:
                baseline_data[kg]['languages_share'] = langs[languages.keys()[0]]
            elif len(languages) ==  1 and languages.keys()[0] not in langs:
                baseline_data[kg]['languages_share'] = 0
            else:
                counter = []
                for l, v in languages.iteritems():
                    if l in langs:
                        counter.extend([langs[l]]*v)
                    else:
                        counter.extend([0]*v)
                baseline_data[kg]['languages_share'] = np.mean(counter)
            for k,v in data.iteritems():
                if not v:
                    baseline_data[kg][k] = 0


        baseline_data = self.normalize_NoCLC('size_subjects', baseline_data)
        baseline_data = self.normalize_NoCLC('size_triples' , baseline_data)
        baseline_data = self.normalize_NoCLC('number_languages' , baseline_data)

        for kg, data in baseline_data.iteritems():
            kg_answers[kg] = np.mean(data.values())

        return kg_answers


    def run_NoCLC(self, query_sets):
        results = []
        for qid_set in query_sets:
            score = self.get_NoCLC(qid_set)
            result = sorted(score.items(), key=operator.itemgetter(1), reverse=True)
            results.append(result)
        return results


    # Distance from ideal
    def run_cos_numbers(self, query_sets):
        results = []
        for qid_set in query_sets:
            distance = self.get_cos_numbers(qid_set)
            result = sorted(distance.items(), key=operator.itemgetter(1), reverse=True)
            results.append(result)
        return results

    # Distance from ideal
    def run_cos(self, query_sets):
        results = []
        for qid_set in query_sets:
            distance = self.get_cos(qid_set)
            result = sorted(distance.items(), key=operator.itemgetter(1), reverse=True)
            results.append(result)
        return results


    # Run to return MSQE
    def run_mse(self, query_sets):
        results = []
        for qid_set in query_sets:
            errors = self.get_errors(qid_set)
            result = sorted(errors.items(), key=operator.itemgetter(1), reverse=True)
            results.append(result)
        return results

class RDFMTRanker:

    def __init__(self, rdfmts):
        self.rdfmts = rdfmts
        self.query_ids = json.load(open('data/query-ids.json'))
        classes = json.load(open('data/classes.json'))
        self.classes = {k.lower(): v for k, v in classes.items()}

    def normalize(self, mts, metric):
        m = []
        for qid, data in mts.iteritems():
            for kgname, d in data.iteritems():
                if d == 0 or not metric in d:
                    continue
                m.append(d[metric])
        if not m:
            return mts
        m_x = [0 if not x else x for x in m]
        if not max(m_x):
            return mts
        maxi = float(max(m_x))
        for qid, data in mts.iteritems():
            for kgname, d in data.iteritems():
                if not d or not metric in d:
                    continue
                if not d[metric]:
                    d[metric] = 0
                    continue
                d[metric] = d[metric]/maxi
        return mts

    def get_average_data(self, mts, lang):
        res = {}
        result = {}
        for mt in mts:
            for k, v in mt.iteritems():
                if k == 'languages_share':
                    if k in res:
                        if not lang in v:
                            res[k].append(0)
                        else:
                            res[k].append(v[lang])
                    else:
                        if not lang in v:
                            res[k] = [0]
                        else:
                            res[k] = [v[lang]]
                else:
                    if k in res:
                        if not v:
                            res[k].append(0)
                        else:
                            res[k].append(v)
                    else:
                        if not v:
                            res[k] = [0]
                        else:
                            res[k] = [v]
        for k, v in res.iteritems():
            result[k] = np.mean(v)
        return result

    def sum_domain(self, res, datalen):
        result = {}
        for id, kgs in res.iteritems():
            for kgname, data in kgs.iteritems():
                if not kgname in result:
                    result[kgname] = {}
                if not data:
                    continue
                for k,v in data.iteritems():
                    if k in result[kgname]:
                        result[kgname][k].append(v)
                    else:
                        result[kgname][k] = [v]

        r = {}
        for kgname, data in result.iteritems():
            r[kgname] = {}
            if not data:
                continue
            for k,v in data.iteritems():
                r[kgname][k] = sum(v) / datalen
        return r


    def get_rdfmts(self, qset):
        results = {}
        for qid, lang in qset.iteritems():
            results[qid] = {}
            for kgname, rdfmt in self.rdfmts.iteritems():
                kgname = kgname.lower()
                results[qid][kgname] = []
                if not str(qid) in self.classes[kgname] or not self.classes[kgname][str(qid)]:
                    results[qid][kgname] = 0
                    continue
                cls = set(self.classes[kgname][str(qid)])
                mts = []
                for c in cls:
                    if kgname == 'yago':
                        c = c.replace('http://yago-knowledge.org/resource/', '')
                    elif 'http' not in c:
                        continue
                    if c not in rdfmt:
                        continue

                    mts.append(rdfmt[c])

                results[qid][kgname] = self.get_average_data(mts, lang)

        results = self.normalize(results, 'size_subjects')
        results = self.normalize(results, 'size_triples')
        results = self.normalize(results, 'number_languages')
        results = self.normalize(results, 'ds_size_triples')

        return results

    def get_scores(self, rdfmts_aggr, metrics):
        result = {}
        for kgname, data in rdfmts_aggr.iteritems():
            result[kgname] = 0
            for key, value in data.iteritems():
                if key in metrics:
                    result[kgname] += value

        res = {}
        for key, value in result.iteritems():
            res[key] = value / len(metrics)
        return  res




    def run(self, query_sets):
        results = []
        metrics_mono = ['ds_size_triples', 'size_subjects', 'size_triples', 'languages_share', 'subject_labeling', 'ds_class_labeling', 'unambiguity']
        metrics_multi = ['ds_size_triples', 'size_subjects', 'size_triples', 'languages_share',
                         'subject_labeling', 'ds_class_labeling', 'unambiguity', 'number_languages', #'entities_1_lang',
                         'entities_2_5_lang', 'entities_6_10_lang', 'entities_11_50_lang', 'entities_50+_lang']
        for qset in query_sets:
            rdfmts = self.get_rdfmts(qset)
            rdfmts_aggr = self.sum_domain(rdfmts, len(qset))

            if len(set(qset.values())) == 1:
                scores = self.get_scores(rdfmts_aggr, metrics_mono)
            else:
                print 'Multilingual ' + str(qset.values())
                scores = self.get_scores(rdfmts_aggr, metrics_multi)

            result = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
            results.append(result)
        return results


# Class to get the ranking for the gold standard for a given set of queries
class GoldStandardRanker:

    def __init__(self, gold_en, gold_es, gold_hi):
        self.gold_en = gold_en
        self.gold_es = gold_es
        self.gold_hi = gold_hi
        self.kgs = ['wikidata', 'dbpedia', 'yago', 'linkedmdb', 'musicbrainz']

    def rename_kgs(self, kgs):
        result = []
        for kg in kgs:
            if kg == 'wd':
                result.append('wikidata')
            elif kg == 'db':
                result.append('dbpedia')
            elif kg == 'yg':
                result.append('yago')
            elif kg == 'linked':
                result.append('linkedmdb')
            elif kg == 'mb':
                result.append('musicbrainz')
        return result

    def normalize(self, kgs, whole):
        result = {}
        for kg, value in kgs.iteritems():
            result[kg] = value/float(whole)
        return result

    def get_gold_ranking(self, qset):
        results = []
        for key, value in qset.iteritems():
            key = str(key)
            r = ''
            if value == 'en' and key in self.gold_en:
                r = self.gold_en[key]
            elif value == 'es' and key in self.gold_es:
                r = self.gold_es[key]
            elif value == 'hi' and key in self.gold_hi:
                r = self.gold_hi[key]
            if ',' in r:
                results.extend([x.strip() for x in r.split(',')])
            elif r:
                results.append(r.strip())

        ranking = self.normalize(Counter(self.rename_kgs(results)), len(qset))
        for kg in self.kgs:
            if kg not in ranking.keys():
                ranking[kg] = 0
        return ranking



    def run(self, query_sets):
        results = []
        for qset in query_sets:
            gold_scores = self.get_gold_ranking(qset)
            result = sorted(gold_scores.items(), key=operator.itemgetter(1), reverse=True)
            results.append(result)
        return results



