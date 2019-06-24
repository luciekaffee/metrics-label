from SPARQLWrapper import SPARQLWrapper, JSON
import json
import itertools
import os

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

classes = {}
data = {}
with open('classes.json') as infile:
    data = json.load(infile)
    data = {k.lower(): v for k, v in data.items()}

kgs = {'dbpedia': 'http://node1.research.tib.eu:4001/sparql', 'linkedmdb': 'http://node3.research.tib.eu:11887/sparql'}

queries = {}
#queries['Q1'] = 'SELECT COUNT(*) WHERE { ?s ?p ?o }'
#queries['Q2'] = 'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT  ?p (COUNT(?s) AS ?counter) { ?s ?p ?o . ?p rdfs:subPropertyOf rdfs:label . }  GROUP BY (?p) ORDER BY DESC(?counter)'
#queries['Q3'] = 'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT COUNT(distinct ?o) { ?s a ?o . ?o rdfs:label ?title .}'
#queries['Q4'] = 'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT COUNT(distinct ?o) { ?s a ?o . }'
#queries['Q5'] = 'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT COUNT(distinct ?p) { ?s ?p ?o . }'
#queries['Q6'] = 'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT COUNT(distinct ?p) { ?s ?p ?o . ?p rdfs:label ?title . }'

#queries['Q7'] = 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> SELECT (COUNT(*) AS ?c) WHERE { ?s rdf:type <%s> . ?s ?p ?o .}'
#queries['Q8'] = 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> SELECT (COUNT(DISTINCT ?item) AS ?c) WHERE { ?item rdf:type <%s>. }'
#queries['Q9'] = 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> SELECT (COUNT(DISTINCT ?item) AS ?c) WHERE  { ?item rdf:type <%s>. ?item rdfs:label ?x . }'
#queries['Q10'] = 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> SELECT ?lt (COUNT(?o) AS ?c) {?o rdf:type <%s> . ?o rdfs:label ?title . BIND (LCASE(lang(?title)) as ?lt) } GROUP BY ?lt'
#queries['Q11'] = 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> SELECT (count(distinct ?lt) AS ?c) {?o rdf:type <%s> . ?o rdfs:label ?title . BIND (LCASE(lang(?title)) as ?lt) }'
#queries['Q12'] = 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> SELECT (count(distinct ?s) AS ?c) { ?s rdf:type <%s> . ?subproperty rdfs:subPropertyOf rdfs:label . ?s rdfs:label ?title . ?s ?subproperty ?otherTitle . FILTER (?title != ?otherTitle) }'
queries['Q13'] = 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> SELECT (COUNT(?count) AS ?c) { SELECT ?s (count(distinct ?lt) as ?count) { ?s rdf:type <%s> . ?s rdfs:label ?title . BIND (LCASE(lang(?title)) as ?lt) } GROUP BY ?s HAVING (count(distinct ?lt) = 1) }'
queries['Q14'] = 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> SELECT (COUNT(?count) AS ?c) { SELECT ?s (count(distinct ?lt) as ?count) { ?s rdf:type <%s> . ?s rdfs:label ?title . BIND (LCASE(lang(?title)) as ?lt) } GROUP BY ?s HAVING ((count(distinct ?lt) > 1) && (count(distinct ?lt) < 6)) }'
queries['Q15'] = 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> SELECT (COUNT(?count) AS ?c) { SELECT ?s (count(distinct ?lt) as ?count) { ?s rdf:type <%s> . ?s rdfs:label ?title . BIND (LCASE(lang(?title)) as ?lt) } GROUP BY ?s HAVING ((count(distinct ?lt) > 5)&& (count(distinct ?lt) < 11)) }'
queries['Q16'] = 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> SELECT (COUNT(?count) AS ?c) { SELECT ?s (count(distinct ?lt) as ?count) { ?s rdf:type <%s> . ?s rdfs:label ?title . BIND (LCASE(lang(?title)) as ?lt) } GROUP BY ?s HAVING ((count(distinct ?lt) > 10) && (count(distinct ?lt) < 51)) }'
queries['Q17'] = 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> SELECT (COUNT(?count) AS ?c) { SELECT ?s (count(distinct ?lt) as ?count) { ?s rdf:type <%s> . ?s rdfs:label ?title . BIND (LCASE(lang(?title)) as ?lt) } GROUP BY ?s HAVING (count(distinct ?lt) > 50) }'

for kg, enpoint in kgs.iteritems():
    print kg
    classes = list(set(list(itertools.chain(*data[kg].values()))))
    for key, q in queries.iteritems():
        print '--------------> ' + key
        if int(key.replace('Q', '')) < 7:
            result = send_query(q, endpoint)
            res = []
            if not result:
                print q
                continue
            for r in result["results"]["bindings"]:
                res.append(r)
            filename = kg + '/' + key + '---' + kg + '.json'
            #if not os.path.exists(os.path.dirname(filename)):
            #    os.makedirs(os.path.dirname(filename))
            with open(filename, 'w+') as outfile:
                json.dump(res, outfile)
            continue

        for c in classes:
            filename = kg + '/' + key + '/' + c.replace('/', '_').replace(' ', '-') + '.json'
            if not os.path.exists(os.path.dirname(filename)):
                os.makedirs(os.path.dirname(filename))
            query = q.replace('%s', c)
            result = send_query(query, enpoint)
            res = []
            if not result:
                with open(filename, 'w+') as outfile:
                    json.dump([], outfile)
                continue
            for r in result["results"]["bindings"]:
                if not 'c' in r:
                    continue
                elif 'lt' in r:
                    res.append({r['lt']['value']: r['c']['value']})
                else:
                    res.append(r['c']['value'])

            with open(filename, 'w+') as outfile:
                json.dump(res, outfile)



