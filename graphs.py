import matplotlib.pyplot as plt
import csv
import numpy as np
import os


# LANGUAGE COUNTS
def get_language_data_Q7(filename):
    data = {}
    with open(filename) as infile:
        reader = csv.reader(infile)
        next(reader) # skip header
        for r in reader:
            data[r[0].replace('"', '')] = int(r[1].replace('"', ''))
    return data


# histogram
def run_language_histogram(data):
    fig, ax = plt.subplots()
    ax.set_yscale('log')
    plt.hist(data.values(), normed=True, bins=30)
    plt.show()


# barchart per language
def run_bar_chart_languages(data):
    data_keys_limited = sorted(data, key=data.get,reverse=True)[:50]
    data_values_limited = []
    for k in data_keys_limited:
        data_values_limited.append(data[k])

    ypos = np.arange(len(data_keys_limited))
    fig, ax = plt.subplots()

    plt.title('Top 50 languages (rdfs:label)')
    ax.bar(ypos, data_values_limited, align='center', alpha=0.5)

    ax.set_xlabel('Languages by language code')
    plt.xticks(ypos, data_keys_limited, rotation='vertical')

    ax.set_ylabel('Number entity labels in language (log)')
    ax.set_yscale('log')

    plt.show()

data = get_language_data_Q7('Q7-res.csv')
run_language_histogram(data)
run_bar_chart_languages(data)


# LANGUAGE COUNTS FOR DIFFERENT DOMAINS

#get keys for the ordering of languages from the general domain data
def get_keys():
    data = {}
    with open('Q7-res.csv') as infile:
        reader = csv.reader(infile)
        next(reader) # skip header
        for r in reader:
            data[r[0].replace('"', '')] = int(r[1].replace('"', ''))
        return sorted(data, key=data.get, reverse=True)[:50]

def calculate_average_by_domain(keys):
    domainfiles = {}
    for filename in os.listdir('Domains'):
        if filename.startswith('Q7-'):
            domain = filename.split('-')[1]
            if domain in domainfiles:
                domainfiles[domain].append(filename)
            else:
                domainfiles[domain] = [filename]
    domaindata = {}
    for domain, filelist in domainfiles:
        for f in filelist
            with open('Domains/' + f):
                data = get_language_data_Q7(f)
                for k in keys:
                    if k in data:
                        if domain in domaindata:
                            domaindata[domain][k] += data[k]
                            domaindata[domain]['counter'] += 1
                        else:
                            domaindata[domain] = {}
                            domaindata[domain][k] = data[k]
                            domaindata[domain]['counter'] = 0
    return domaindata

#@todo: generate the graph with multiple, labeled subgraphs
def run_graph_languages_domains(keys, domaindata):
    for k in keys:
        return k



