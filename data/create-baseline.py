
from SPARQLWrapper import SPARQLWrapper, JSON
import json
import itertools


kgs = {'linkedmdb': 'http://node3.research.tib.eu:11887/sparql', 'dbpedia': 'http://node1.research.tib.eu:4001/sparql', 'wikidata': 'http://node3.research.tib.eu:4010/sparql', 'yago': 'http://node3.research.tib.eu:4011/sparql', 'musicbrainz': 'http://node3.research.tib.eu:4012/sparql'}

queries = {}

queries['Q1'] = 'SELECT COUNT(*) WHERE { ?s ?p ?o }'
#queries['Q2'] = 'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT ?p (COUNT(?s) AS ?counter) { ?s ?p ?o . ?p rdfs:subPropertyOf rdfs:label . }  GROUP BY (?p) ORDER BY DESC(?counter)'
queries['Q3'] = 'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT COUNT(distinct ?o) { ?s a ?o . ?o rdfs:label ?title .}'
queries['Q4'] = 'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT COUNT(distinct ?o) { ?s a ?o . }'
#queries['Q5'] = 'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT COUNT(distinct ?p) { ?s ?p ?o . }'
#queries['Q6'] = 'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT COUNT(distinct ?p) { ?s ?p ?o . ?p rdfs:label ?title . }'

queries['Q8'] = 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> SELECT (COUNT(DISTINCT ?item) AS ?c) WHERE { ?item ?p ?o. }'
queries['Q9'] = 'SELECT (COUNT(DISTINCT ?item) AS ?c) WHERE  { ?item rdfs:label ?x . }'
queries['Q10'] = 'SELECT ?lt (COUNT(?o) AS ?c) { ?o rdfs:label ?title . BIND (LCASE(lang(?title)) as ?lt) } GROUP BY ?lt'
queries['Q11'] = 'SELECT (count(distinct ?lt) AS ?c) { ?o rdfs:label ?title . BIND (LCASE(lang(?title)) as ?lt) }'
queries['Q12'] = 'SELECT (count(distinct ?s) AS ?c) { ?subproperty rdfs:subPropertyOf rdfs:label . ?s rdfs:label ?title . ?s ?subproperty ?otherTitle . FILTER (?title != ?otherTitle) }'

queries['Q13'] = 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> SELECT (COUNT(?count) AS ?c) { SELECT ?s (count(distinct ?lt) as ?count) {?s rdfs:label ?title . BIND (LCASE(lang(?title)) as ?lt) } GROUP BY ?s HAVING (count(distinct ?lt) = 1) }'
queries['Q14'] = 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> SELECT (COUNT(?count) AS ?c) { SELECT ?s (count(distinct ?lt) as ?count) {?s rdfs:label ?title . BIND (LCASE(lang(?title)) as ?lt) } GROUP BY ?s HAVING ((count(distinct ?lt) > 1) && (count(distinct ?lt) < 6)) }'
queries['Q15'] = 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> SELECT (COUNT(?count) AS ?c) { SELECT ?s (count(distinct ?lt) as ?count) {?s rdfs:label ?title . BIND (LCASE(lang(?title)) as ?lt) } GROUP BY ?s HAVING ((count(distinct ?lt) > 5)&& (count(distinct ?lt) < 11)) }'
queries['Q16'] = 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> SELECT (COUNT(?count) AS ?c) { SELECT ?s (count(distinct ?lt) as ?count) {?s rdfs:label ?title . BIND (LCASE(lang(?title)) as ?lt) } GROUP BY ?s HAVING ((count(distinct ?lt) > 10) && (count(distinct ?lt) < 51)) }'
queries['Q17'] = 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> SELECT (COUNT(?count) AS ?c) { SELECT ?s (count(distinct ?lt) as ?count) {?s rdfs:label ?title . BIND (LCASE(lang(?title)) as ?lt) } GROUP BY ?s HAVING (count(distinct ?lt) > 50) }'


def send_query(query, endpoint):
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    try:
        result = sparql.query().convert()
    except:
        print query
        result = []
    return result

def create_baseline(baseline_data):
    content = {}
    for kg, data in baseline_data:
        if 'Q1' in data and data['Q1']:
            content['size_triples'] = float(data['Q1'])
        else:
            content['size_triples'] = []
        if 'Q3' in data and 'Q4' in data and data['Q3'] and data['Q4']:
            content['class_labeling'] = float(data['Q3'])/float(data['Q4'])
        else:
            content['class_labeling'] = []
        if 'Q11' in data and data['Q11']:
            content['number_languages'] = float(data['Q11'])
        else:
            content['number_languages'] = []

        if 'Q8' in data and data['Q8']:
            content['size_subjects'] = float(data['Q8'])
        else:
            content['size_subjects'] = []
        if 'Q9' in data and 'Q8' in data and data['Q9'] and data['Q8']:
                content['subject_labeling'] = float(data['Q9'])/float(data['Q8'])
        else:
            content['subject_labeling'] = []
        if 'Q12' in data and 'Q8' in data and data['Q12'] and data['Q8']:
            content['unambiguity'] = float(data['Q12'])/float(data['Q8'])
        else:
            content['unambiguity'] = 1

        content['languages_share'] = {}
        lang_total = 0

        if 'Q10' not in data or not data['Q10']:
            return content

        for lang, value in data['Q10'].iteritems():
            lang_total += float(value)
        for lang, value in data['Q10'].iteritems():
            content['languages_share'][lang] = float(value)/lang_total
        if 'Q13' in data and 'Q8' in data and data['Q13'] and data['Q8']:
            content['entities_1_lang'] = float(data['Q13'])/float(data['Q8'])
        else:
            content['entities_1_lang'] = []
        if 'Q14' in data and 'Q8' in data and data['Q14'] and data['Q8']:
            content['entities_2_5_lang'] = float(data['Q14'])/float(data['Q8'])
        else:
            content['entities_2_5_lang'] = []
        if 'Q15' in data and 'Q8' in data and data['Q15'] and data['Q8']:
            content['entities_6_10_lang'] = float(data['Q15']) / float(data['Q8'])
        else:
            content['entities_6_10_lang'] = []
        if 'Q16' in data and 'Q8' in data and data['Q16'] and data['Q8']:
            content['entities_11_50_lang'] = float(data['Q16']) / float(data['Q8'])
        else:
            content['entities_11_50_lang'] = []
        if 'Q17' in data and 'Q8' in data and data['Q17'] and data['Q8']:
            content['entities_50+_lang'] = float(data['Q17']) / float(data['Q8'])
        else:
            content['entities_50+_lang'] = 0
    return content

baseline_data = {}

for kg, endpoint in kgs.iteritems():
    print kg
    baseline_data[kg] = {}
    for key, q in queries.iteritems():
        baseline_data[kg][key] = []
        print '--------------> ' + key
        result = send_query(q, endpoint)
        for r in result["results"]["bindings"]:
            if 'callret-0' in r:
                baseline_data[kg][key].append(r['callret-0']['value'])
            elif 'lt' in r:
                res.append({r['lt']['value']: r['c']['value']})
            elif 'c' in r:
                baseline_data[kg][key].append(r['c']['value'])
            else:
                print r
    print baseline_data

json.dump(create_baseline(baseline_data), 'baselines/baseline_kgs_metrics.json')