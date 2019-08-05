from SPARQLWrapper import SPARQLWrapper, JSON
import json
import itertools
import os

class EnpointPreparerBio2RDF():
    def __init__(self):
        self.endpoints = {}
        self.endpoints['bio2rdf_wormbase'] = 'http://node4.research.tib.eu:1370/sparql'
        self.endpoints['bio2rdf_taxonomy'] = 'http://node4.research.tib.eu:1371/sparql'
        self.endpoints['bio2rdf_iproclass'] = 'http://node4.research.tib.eu:1372/sparql'
        self.endpoints['bio2rdf_homologene'] = 'http://node4.research.tib.eu:1373/sparql'
        self.endpoints['bio2rdf_goa'] = 'http://node4.research.tib.eu:1374/sparql'
        self.endpoints['bio2rdf_genage'] = 'http://node4.research.tib.eu:1375/sparql'
        self.endpoints['bio2rdf_dbsnp'] = 'http://node4.research.tib.eu:1376/sparql'
        self.endpoints['bio2rdf_clinicaltrials'] = 'http://node4.research.tib.eu:1377/sparql'
        self.endpoints['bio2rdf_bioportal'] = 'http://node4.research.tib.eu:1378/sparql'
        self.endpoints['bio2rdf_kegg'] = 'http://node4.research.tib.eu:1379/sparql'
        self.endpoints['bio2rdf_lsr'] = 'http://node4.research.tib.eu:1380/sparql'
        self.endpoints['bio2rdf_mesh'] = 'http://node4.research.tib.eu:1381/sparql'
        self.endpoints['bio2rdf_linkedspl'] = 'http://node4.research.tib.eu:1382/sparql'
        self.endpoints['bio2rdf_irefindex'] = 'http://node4.research.tib.eu:1383/sparql'
        self.endpoints['bio2rdf_interpro'] = 'http://node4.research.tib.eu:1384/sparql'
        self.endpoints['bio2rdf_ncbigene'] = 'http://node4.research.tib.eu:1385/sparql'
        self.endpoints['bio2rdf_omim'] = 'http://node4.research.tib.eu:1386/sparql'
        self.endpoints['bio2rdf_pathwaycommons'] = 'http://node4.research.tib.eu:1387/sparql'
        self.endpoints['bio2rdf_reactome'] = 'http://node4.research.tib.eu:1388/sparql'
        self.endpoints['bio2rdf_sgd'] = 'http://node4.research.tib.eu:1389/sparql'
        self.endpoints['bio2rdf_orphanet'] = 'http://node4.research.tib.eu:1390/sparql'
        self.endpoints['bio2rdf_ndc'] = 'http://node4.research.tib.eu:1391/sparql'
        self.endpoints['bio2rdf_mgi'] = 'http://node4.research.tib.eu:1392/sparql'
        self.endpoints['bio2rdf_wikipathways'] = 'http://node4.research.tib.eu:1393/sparql'
        self.endpoints['bio2rdf_sider'] = 'http://node4.research.tib.eu:1394/sparql'
        self.endpoints['bio2rdf_sabiork'] = 'http://node4.research.tib.eu:1395/sparql'
        self.endpoints['bio2rdf_pharmgkb'] = 'http://node4.research.tib.eu:1396/sparql'
        self.endpoints['bio2rdf_hgnc'] = 'http://node4.research.tib.eu:1397/sparql'
        self.endpoints['bio2rdf_gendr'] = 'http://node4.research.tib.eu:1398/sparql'
        self.endpoints['bio2rdf_drugbank'] = 'http://node4.research.tib.eu:1399/sparql'
        self.endpoints['bio2rdf_ctd'] = 'http://node4.research.tib.eu:1400/sparql'
        self.endpoints['bio2rdf_chembl'] = 'http://node4.research.tib.eu:1401/sparql'
        self.endpoints['bio2rdf_affymetrix'] = 'http://node4.research.tib.eu:1402/sparql'
        self.endpoints['bio2rdf_biomodels'] = 'http://node4.research.tib.eu:1403/sparql'
        self.endpoints['bio2rdf_pubmedr4'] = 'http://node4.research.tib.eu:1404/sparql'

    def run(self):
        return self.endpoints

class EnpointPreparerLSLOD():
    def __init__(self):
        self.endpoints = {}
        self.endpoints['sider'] = 'http://node4.research.tib.eu:11360/sparql'
        self.endpoints['affymetrix'] = 'http://node4.research.tib.eu:11361/sparql'
        self.endpoints['chebi'] = 'http://node4.research.tib.eu:11362/sparql'
        self.endpoints['dailymed'] = 'http://node4.research.tib.eu:11363/sparql'
        self.endpoints['diseasome'] = 'http://node4.research.tib.eu:11364/sparql'
        self.endpoints['drugbank'] = 'http://node4.research.tib.eu:11365/sparql'
        self.endpoints['kegg'] = 'http://node4.research.tib.eu:11366/sparql'
        self.endpoints['linkedct'] = 'http://node4.research.tib.eu:11367/sparql'
        self.endpoints['linkedtcga'] = 'http://node4.research.tib.eu:11368/sparql'
        self.endpoints['medicare'] = 'http://node4.research.tib.eu:11369/sparql'

    def run(self):
        return self.endpoints

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
        result = self.send_query(query, endpoint)
        for r in result["results"]["bindings"]:
            #if 'class' in r and 'value' in r['class']:
            classes.append(r['class']['value'])
        return classes

    def write_results(self, classes, kg, endpoint):
        if not os.path.exists('data/raw/' + kg):
            os.makedirs('data/raw/' + kg)
        for key, q in self.queries.iteritems():
            print '--------------> ' + key

            if int(key.replace('Q', '')) < 7:
                result = self.send_query(q, endpoint)
                res = []
                if not result:
                    print q
                    continue
                for r in result["results"]["bindings"]:
                    res.append(r)
                filename = 'data/raw/' + kg + '/' + key + '.json'
                with open(filename, 'w+') as outfile:
                    json.dump(res, outfile)
                continue

            classdata = {}
            for c in classes:
                query = q.replace('%s', c)
                result = self.send_query(query, endpoint)
                res = []
                if not result:
                    classdata[c] = []
                    continue
                for r in result["results"]["bindings"]:
                    if not 'c' in r:
                        continue
                    elif 'lt' in r:
                        res.append({r['lt']['value']: r['c']['value']})
                    else:
                        res.append(r['c']['value'])
                classdata[c] = res
            filename = 'data/raw/' + kg + '/' + key + '.json'
            with open(filename, 'w+') as outfile:
                json.dump(classdata, outfile)

    def run(self, endpoints, classes=None):
        for kg, endpoint in endpoints.iteritems():
            if not classes:
                classes = self.get_classes(endpoint)
            self.write_results(classes, kg, endpoint)
