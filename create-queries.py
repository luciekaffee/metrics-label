import json


def write_to_file(query_name, domain_name, namespace_name, query_string):
    folder = ''
    if int(query_name.replace('Q', '')) < 8:
        folder = 'Queries-1/'
    elif int(query_name.replace('Q', '')) > 7 and int(query_name.replace('Q', '')) < 13:
        folder = 'Queries-2/'
    else:
        folder = 'Queries-3/'
    with open('Queries/' + folder + query_name + '-' + domain_name + '-' + namespace_name, 'w') as outfile:
        outfile.write(query_string.encode('utf-8').strip())


def generate_queries(domain_name, domain_data, query_patterns):
    for query_name, query_pattern in query_patterns.iteritems():
        for namespace_name, namespace in domain_data.iteritems():
            query_string = query_pattern.replace('XYZNS', '"' + namespace + '"')
            print query_name + '-' + domain_name + '-' + namespace_name, query_string
            write_to_file(query_name, domain_name, namespace_name, query_string)


data = {}
query_patterns = {}

with open('lod-cloud-domains.json') as infile:
    data = json.load(infile)

with open('query-patterns.tsv') as infile:
    next(infile)
    for line in infile:
        tmp = line.strip().split('\t')
        query_patterns[tmp[0]] = tmp[1]

# write each query to a file called FOLDER/Q<query_name>-<domain>-<namespace>
for domain, domain_data in data.iteritems():
    print 'add queries for domain ' + domain
    generate_queries(domain, domain_data, query_patterns)
