import json
import random
import copy
from sklearn.metrics import mean_squared_error
import operator
import numpy as np

class DomainCreator:

    def __init__(self, languages):
        self.query_ids = json.load(open('data/query-ids.json'))
        self.classes = json.load(open('data/classes.json'))
        self.languages = languages

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
                if not str(qid) in self.answers[lang][kg]:
                    kg_answer = 0
                else:
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
            result = sorted(errors.items(), key=operator.itemgetter(1))
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

    def sum_domain(self, res):
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
                r[kgname][k] = np.mean(v)
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
                x = str(qid)
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
                         'subject_labeling', 'ds_class_labeling', 'unambiguity', 'number_languages',
                         'entities_1_lang', 'entities_2_5_lang', 'entities_6_10_lang', 'entities_11_50_lang', 'entities_50+_lang']
        for qset in query_sets:
            scores = {}
            rdfmts = self.get_rdfmts(qset)
            rdfmts_aggr = self.sum_domain(rdfmts)

            if len(set(qset.values())) == 1:
                scores = self.get_scores(rdfmts_aggr, metrics_mono)
            else:
                print 'Multilingual ' + str(qset.values())
                scores = self.get_scores(rdfmts_aggr, metrics_multi)

            result = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
            return result



