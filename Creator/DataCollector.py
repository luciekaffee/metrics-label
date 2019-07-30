from SPARQLWrapper import SPARQLWrapper, JSON
import json
import itertools
import os

class BasicDataCollector():
    def __init__(self):
        self.queries = {}
        self.queries['Q1'] = 'SELECT COUNT(*) WHERE { ?s ?p ?o }'
        self.queries['Q2'] = 'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT  ?p (COUNT(?s) AS ?counter) { ?s ?p ?o . ?p rdfs:subPropertyOf rdfs:label . }  GROUP BY (?p) ORDER BY DESC(?counter)'
        self.queries['Q3'] = 'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT COUNT(distinct ?o) { ?s a ?o . ?o rdfs:label ?title .}'
        self.queries['Q4'] = 'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT COUNT(distinct ?o) { ?s a ?o . }'
        self.queries['Q5'] = 'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT COUNT(distinct ?p) { ?s ?p ?o . }'
        self.queries['Q6'] = 'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT COUNT(distinct ?p) { ?s ?p ?o . ?p rdfs:label ?title . }'

        self.queries['Q7'] = 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> SELECT (COUNT(*) AS ?c) WHERE { ?s rdf:type <%s> . ?s ?p ?o .}'
        self.queries['Q8'] = 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> SELECT (COUNT(DISTINCT ?item) AS ?c) WHERE { ?item rdf:type <%s>. }'
        self.queries['Q9'] = 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> SELECT (COUNT(DISTINCT ?item) AS ?c) WHERE  { ?item rdf:type <%s>. ?item rdfs:label ?x . }'
        self.queries['Q10'] = 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> SELECT ?lt (COUNT(?o) AS ?c) {?o rdf:type <%s> . ?o rdfs:label ?title . BIND (LCASE(lang(?title)) as ?lt) } GROUP BY ?lt'
        self.queries['Q11'] = 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> SELECT (count(distinct ?lt) AS ?c) {?o rdf:type <%s> . ?o rdfs:label ?title . BIND (LCASE(lang(?title)) as ?lt) }'
        self.queries['Q12'] = 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> SELECT (count(distinct ?s) AS ?c) { ?s rdf:type <%s> . ?subproperty rdfs:subPropertyOf rdfs:label . ?s rdfs:label ?title . ?s ?subproperty ?otherTitle . FILTER (?title != ?otherTitle) }'
        self.queries['Q13'] = 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> SELECT (COUNT(?count) AS ?c) { SELECT ?s (count(distinct ?lt) as ?count) { ?s rdf:type <%s> . ?s rdfs:label ?title . BIND (LCASE(lang(?title)) as ?lt) } GROUP BY ?s HAVING (count(distinct ?lt) = 1) }'
        self.queries['Q14'] = 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> SELECT (COUNT(?count) AS ?c) { SELECT ?s (count(distinct ?lt) as ?count) { ?s rdf:type <%s> . ?s rdfs:label ?title . BIND (LCASE(lang(?title)) as ?lt) } GROUP BY ?s HAVING ((count(distinct ?lt) > 1) && (count(distinct ?lt) < 6)) }'
        self.queries['Q15'] = 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> SELECT (COUNT(?count) AS ?c) { SELECT ?s (count(distinct ?lt) as ?count) { ?s rdf:type <%s> . ?s rdfs:label ?title . BIND (LCASE(lang(?title)) as ?lt) } GROUP BY ?s HAVING ((count(distinct ?lt) > 5)&& (count(distinct ?lt) < 11)) }'
        self.queries['Q16'] = 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> SELECT (COUNT(?count) AS ?c) { SELECT ?s (count(distinct ?lt) as ?count) { ?s rdf:type <%s> . ?s rdfs:label ?title . BIND (LCASE(lang(?title)) as ?lt) } GROUP BY ?s HAVING ((count(distinct ?lt) > 10) && (count(distinct ?lt) < 51)) }'
        self.queries['Q17'] = 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> SELECT (COUNT(?count) AS ?c) { SELECT ?s (count(distinct ?lt) as ?count) { ?s rdf:type <%s> . ?s rdfs:label ?title . BIND (LCASE(lang(?title)) as ?lt) } GROUP BY ?s HAVING (count(distinct ?lt) > 50) }'

    def send_query(self, query, endpoint):
        sparql = SPARQLWrapper(endpoint)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        try:
            result = sparql.query().convert()
        except:
            print query
            result = []
        return result

    def get_classes(self, endpoint):
        classes = []
        query = 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> SELECT DISTINCT ?class WHERE { ?s rdf:type ?class . }'
        result = self.send_query(query)
        for r in result["results"]["bindings"]:
            #if 'class' in r and 'value' in r['class']:
            classes.append(r['class']['value'])
                        