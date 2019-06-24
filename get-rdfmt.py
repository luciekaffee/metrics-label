import json
from SPARQLWrapper import SPARQLWrapper, JSON


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


query_rdfmts = 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> SELECT DISTINCT ?class WHERE {?item rdf:type ?class .}'
query_rdfmts_wd = 'PREFIX wdt: <http://www.wikidata.org/prop/direct/> SELECT DISTINCT ?class WHERE {?item wdt:P31 ?class .}'


results = send_query(query_rdfmts, 'http://node1.research.tib.eu:4001/sparql')
dbpedia_classes = []
for result in results["results"]["bindings"]:
    dbpedia_classes.append(result["class"]["value"])

json.dumps(dbpedia_classes, 'classes/dbpedia.json')

results = send_query(query_rdfmts, 'http://node3.research.tib.eu:4011/sparql')
yago_classes = []
for result in results["results"]["bindings"]:
    yago_classes.append(result["class"]["value"])

json.dumps(yago_classes, 'classes/yago.json')

results = send_query(query_rdfmts, 'http://node3.research.tib.eu:4012/sparql')
mb_classes = []
for result in results["results"]["bindings"]:
    mb_classes.append(result["class"]["value"])

json.dumps(mb_classes, 'classes/musicbrainz.json')

results = send_query(query_rdfmts, 'http://node3.research.tib.eu:11887/sparql')
linked_classes = []
for result in results["results"]["bindings"]:
    linked_classes.append(result["class"]["value"])

json.dumps(linked_classes, 'classes/linkedmdb.json')

results = send_query(query_rdfmts_wd, 'https://query.wikidata.org/sparql')
wd_classes = []
for result in results["results"]["bindings"]:
    wd_classes.append(result["class"]["value"])

json.dumps(wd_classes, 'classes/wikidata.json')
