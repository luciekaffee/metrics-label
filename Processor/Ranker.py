import json
import random
import copy
from sklearn.metrics import mean_squared_error
import operator
import numpy as np

class DomainCreator:

    def __init__(self):
        self.query_ids = json.load(open('data/query-ids.json'))
        self.classes = json.load(open('data/classes.json'))
        self.languages = ['en', 'ar', 'es']

    def get_qids_from_classes(self, kg):
        qids = {}
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
        random.shuffle(qids)
        for q in qids[:number_queries]:
            if lang:
                result[q] = lang
            else:
                result[q] = random.choice(self.languages)
        return result

    # Options for domains: Music, Film
    # Language options are either en, ar, es or None, so it will pick a language for each query at random
    def run(self, number_queries, number_sets, domains=None, language=None):
        queries_result = []
        if not domains:
            for x in range(0, number_sets):
                queries_result.append(self.get_queries_all(number_queries, language))

        elif domains == 'Music':
            qids = self.get_qids_from_classes('MusicBrainz')
            for x in range(0, number_sets):
                queries_result.append(self.get_queries_selected(qids, number_queries, language))

        elif domains == 'Film':
            qids = self.get_qids_from_classes('linkedmdb')
            for x in range(0, number_sets):
                queries_result.append(self.get_queries_selected(qids, number_queries, language))
        else:
            print 'Please add a valid domain, either "Music" or "Film"'

        return queries_result

class AnswerCompletenessRanker:

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

    def get_errors(self, qid_set):
        kg_answers = {}
        gold_answers = []
        for qid, lang in qid_set.iteritems():
            gold_answers.append(self.answers_numbers[str(qid)])
        for kg in self.kgs:
            kg_answers[kg] = []
            for qid, lang in qid_set.iteritems():
                kg_answer = len(self.answers[lang][kg][str(qid)])
                #if kg_answer == 0:

                kg_answers[kg].append(kg_answer)
        errors = {}
        for kg, e in kg_answers.iteritems():
            errors[kg] = mean_squared_error(gold_answers, e)
        return errors

    def run(self, query_sets):
        results = []
        for set in query_sets:
            errors = self.get_errors(set)
            result = sorted(errors.items(), key=operator.itemgetter(0))
            results.append(result)
        return results

class RDFMTRanker:

    def __init__(self, rdfmts):
        self.rdfmts = rdfmts
        self.query_ids = json.load(open('data/query-ids.json'))
        self.classes = json.load(open('data/classes.json'))

    def normalize(self, mts, metric):
        m = []
        for qid, data in mts:
            for kgname, d in data:
                m.append(d[metric])
        maxi = float(max(m))
        for qid, data in mts:
            for kgname, d in data:
                d[metric] = d[metric]/maxi
        return mts

    def get_average_data(self, mts):
        res = {}
        result = {}
        for mt in mts:
            for k, v in mt.iteritems():
                if k == 'languages_share' or not v:
                    continue
                if k in res:
                    res[k].append(v)
                else:
                    res[k] = [v]
        for k, v in res.iteritems():
            result[k] = np.mean(v)
        return result

    def get_rdfmts(self, set):
        results = []
        for qid in set:
            results[qid] = {}
            for kgname, rdfmt in self.rdfmts:
                results[qid][kgname] = []
                cls = set(self.classes[kgname][str(qid)])
                mts = []
                for c in cls:
                    if kgname == 'YAGO':
                        c = c.replace('http://yago-knowledge.org/resource/', '')
                    elif 'http' not in c:
                        continue
                    if c not in rdfmt:
                        # print kgname, cls
                        continue
                    mts.append(rdfmt[c])
                if len(mts) > 1:
                    results[qid][kgname] = self.get_average_data(mts)
                elif len(mts) == 1:
                    results[qid][kgname] = mts[0]
        results = self.normalize(results, 'languages_share')
        results = self.normalize(results, 'size_triples')

        return results

    def get_metrics_results(self, set):
        return self.get_rdfmts(set)

    def run(self, query_sets, language='None'):
        results = []
        for set in query_sets:
            print self.get_metrics_results(set)
            #if language:
            #    metrics = self.get_metrics_results(set)
            #    result = sorted(metrics.items(), key=operator.itemgetter(0))
            #    results.append(result)
            #else:
            #    metrics = self.get_metrics_results_multilingual(set)
            #    result = sorted(metrics.items(), key=operator.itemgetter(0))
            #    results.append(result)


