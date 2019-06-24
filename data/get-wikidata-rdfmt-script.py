from SPARQLWrapper import SPARQLWrapper, JSON
import json
import itertools

def send_query(query, endpoint):
	query = 'PREFIX wdt: <http://www.wikidata.org/prop/direct/> ' + query
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    try:
        result = sparql.query().convert()
    except:
        result = []
        print query
    return result

classes = {}

with open('classes.json') as infile:
	data = json.load(infile)
	classes = list(set(list(itertools.chain(*data['wikidata'].values()))))

queries = {}
#queries['Q1'] = 'SELECT COUNT(*) WHERE { ?s ?p ?o }'
#queries['Q2'] = 'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT ?p (COUNT(?s) AS ?counter) { ?s ?p ?o . ?p rdfs:subPropertyOf rdfs:label . }  GROUP BY (?p) ORDER BY DESC(?counter)'
#queries['Q3'] = 'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT COUNT(distinct ?o) { ?s a ?o . ?o rdfs:label ?title .}'
#queries['Q4'] = 'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT COUNT(distinct ?o) { ?s a ?o . }'
#queries['Q5'] = 'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT COUNT(distinct ?p) { ?s ?p ?o . }'
#queries['Q6'] = 'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT COUNT(distinct ?p) { ?s ?p ?o . ?p rdfs:label ?title . }'

#queries['Q7'] = 'SELECT (COUNT(*) AS ?c) WHERE { ?s wdt:P31 <%s> . ?s ?p ?o}'
#queries['Q8'] = 'SELECT (COUNT(DISTINCT ?item) AS ?c) WHERE { ?item wdt:P31 <%s>. }'
#queries['Q9'] = 'SELECT (COUNT(DISTINCT ?item) AS ?c) WHERE  { ?item wdt:P31 <%s>. ?item rdfs:label ?x . }'
#queries['Q10'] = 'SELECT ?lt (COUNT(?o) AS ?c) {?o wdt:P31 <%s> . ?o rdfs:label ?title . BIND (LCASE(lang(?title)) as ?lt) } GROUP BY ?lt'
#queries['Q11'] = 'SELECT (count(distinct ?lt) AS ?c) {?o wdt:P31 <%s> . ?o rdfs:label ?title . BIND (LCASE(lang(?title)) as ?lt) }'
#queries['Q12'] = 'SELECT (count(distinct ?s) AS ?c) { ?s wdt:P31 <%s> . ?subproperty rdfs:subPropertyOf rdfs:label . ?s rdfs:label ?title . ?s ?subproperty ?otherTitle . FILTER (?title != ?otherTitle) }'
queries['Q13'] = 'SELECT (COUNT(?count) AS ?c) { SELECT ?s (count(distinct ?lt) as ?count) { ?s wdt:P31 <%s> . ?s rdfs:label ?title . BIND (LCASE(lang(?title)) as ?lt) } GROUP BY ?s HAVING (count(distinct ?lt) = 1) }'
queries['Q14'] = ' SELECT (COUNT(?count) AS ?c) { SELECT ?s (count(distinct ?lt) as ?count) { ?s wdt:P31 <%s> . ?s rdfs:label ?title . BIND (LCASE(lang(?title)) as ?lt) } GROUP BY ?s HAVING ((?count > 1) && (?count < 6)) }'
queries['Q15'] = 'SELECT (COUNT(?count) AS ?c) { SELECT ?s (count(distinct ?lt) as ?count) { ?s wdt:P31 <%s> . ?s rdfs:label ?title . BIND (LCASE(lang(?title)) as ?lt) } GROUP BY ?s HAVING ((?count > 5) && (?count < 11)) }'
queries['Q16'] = 'SELECT (COUNT(?count) AS ?c) { SELECT ?s (count(distinct ?lt) as ?count) { ?s wdt:P31 <%s> . ?s rdfs:label ?title . BIND (LCASE(lang(?title)) as ?lt) } GROUP BY ?s HAVING ((?count > 10) && (?count < 51)) }'
queries['Q17'] = 'SELECT (COUNT(?count) AS ?c) { SELECT ?s (count(distinct ?lt) as ?count) { ?s wdt:P31 <%s> . ?s rdfs:label ?title . BIND (LCASE(lang(?title)) as ?lt) } GROUP BY ?s HAVING (?count > 50) }'

for key, q in queries.iteritems():
	print '--------------> ' + key
	if int(key.replace('Q', '')) < 7:
		result = send_query(q, 'http://node3.research.tib.eu:4010/sparql')
		res = []
		if not result:
			print q
			continue
		for r in result["results"]["bindings"]:
			res.append(r)
		with open('wikidata-results/' + key + '.json', 'w+') as outfile:
			json.dump(res, outfile)
		continue
	for c in classes:
		# Q8: 		SELECT (COUNT(DISTINCT ?item) AS ?c) WHERE { ?item wdt:P31 <%s>. }
		# Q9: SELECT (COUNT(DISTINCT ?item) AS ?c) WHERE  { ?item wdt:P31 <%s>. ?item rdfs:label ?x . }
		# Q10: SELECT ?lt (COUNT(?o) AS ?c) {?o wdt:P31 <%s> . ?o rdfs:label ?title . BIND (LCASE(lang(?title)) as ?lt) } GROUP BY ?lt
		# Q11: SELECT (count(distinct ?lt) AS ?c) {?o wdt:P31 <%s> . ?o rdfs:label ?title . BIND (LCASE(lang(?title)) as ?lt) }
		# Q12: SELECT (count(distinct ?s) AS ?c) { ?s wdt:P31 <%s> . ?subproperty rdfs:subPropertyOf rdfs:label . ?s rdfs:label ?title . ?s ?subproperty ?otherTitle . FILTER (?title != ?otherTitle) }
		# Q13: SELECT (COUNT(?count) AS ?c) { SELECT ?s (count(distinct ?lt) as ?count) { ?s wdt:P31 <%s> . ?s rdfs:label ?title . BIND (LCASE(lang(?title)) as ?lt) } GROUP BY ?s HAVING (count(distinct ?lt) = 1) }
		# Q14: SELECT (COUNT(?count) AS ?c) { SELECT ?s (count(distinct ?lt) as ?count) { ?s wdt:P31 <%s> . ?s rdfs:label ?title . BIND (LCASE(lang(?title)) as ?lt) } GROUP BY ?s HAVING ((?count > 1) && (?count < 6)) }
		# Q15: SELECT (COUNT(?count) AS ?c) { SELECT ?s (count(distinct ?lt) as ?count) { ?s wdt:P31 <%s> . ?s rdfs:label ?title . BIND (LCASE(lang(?title)) as ?lt) } GROUP BY ?s HAVING ((?count > 5) && (?count < 11)) }
		# Q16: SELECT (COUNT(?count) AS ?c) { SELECT ?s (count(distinct ?lt) as ?count) { ?s wdt:P31 <%s> . ?s rdfs:label ?title . BIND (LCASE(lang(?title)) as ?lt) } GROUP BY ?s HAVING ((?count > 10) && (?count < 51)) }
		# Q17: SELECT (COUNT(?count) AS ?c) { SELECT ?s (count(distinct ?lt) as ?count) { ?s wdt:P31 <%s> . ?s rdfs:label ?title . BIND (LCASE(lang(?title)) as ?lt) } GROUP BY ?s HAVING (?count > 50) }
		#query = """
		#	SELECT ?lt (COUNT(?o) AS ?c) {?o wdt:P31 <%s> . ?o rdfs:label ?title . BIND (LCASE(lang(?title)) as ?lt) } GROUP BY ?lt
		#"""
		query = q.replace('%s', c)
		result = send_query(query, 'https://query.wikidata.org/sparql')
		res = []
		if not result:
			with open('wikidata-results/' + key + '/' + c.replace('/', '_').replace(' ', '-') + '.json', 'w+') as outfile:
				json.dump([], outfile)
			continue
		for r in result["results"]["bindings"]:
			if not 'c' in r:
				continue
			elif 'lt' in r:
				res.append({r['lt']['value']: r['c']['value']})
			else:
				res.append(r['c']['value'])
		with open('wikidata-results/' + key + '/' + c.replace('/', '_').replace(' ', '-') + '.json', 'w+') as outfile:
			json.dump(res, outfile)

