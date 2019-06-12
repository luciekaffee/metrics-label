import json
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

wikidata_rdfmt = json.load(open('../data/wikidata-rdfmt.json'))['wikidata']
dbpedia_rdfmt = json.load(open('../data/dbpedia-rdfmt.json'))['dbpedia']
yago_rdfmt = json.load(open('../data/yago-rdfmt.json'))['yago']
linkedmdb_rdfmt = json.load(open('../data/linkedmdb-rdfmt.json'))['linkedmdb']
musicbrainz_rdfmt = json.load(open('../data/musicbrainz-rdfmt.json'))['musicbrainz']

all = [wikidata_rdfmt, dbpedia_rdfmt, yago_rdfmt, linkedmdb_rdfmt, musicbrainz_rdfmt]

# working with average!
def get_language_share(kg_rdfmt):
    res = {}
    result = {}
    for domain, data in kg_rdfmt.iteritems():
        if not 'languages_share' in data:
            continue
        d = data['languages_share']
        for k, v in d.iteritems():
            if k in res:
                res[k].append(v)
            else:
                res[k] = [v]
    for key, value in res.iteritems():
        result[key] = np.mean(value)


def get_all_mts(kg_rdfmt):
    res = {}
    result_avg = {}
    result_median = {}
    for domain, data in kg_rdfmt.iteritems():
        for key, value in data.iteritems():
            if key == 'languages_share' or not value:
                continue
            if key in res:
                res[key].append(value)
            else:
                res[key] = [value]
    for key, value in res.iteritems():
        result_avg[key] = np.mean(value)
    for key, value in res.iteritems():
        result_median[key] = np.median(value)
    return [result_avg, result_median]

def create_barchart(wd, dbpedia, yago, linked, mb, keys):
    N = len(keys)
    fig, ax = plt.subplots()
    width = 0.35
    ind = np.arange(N)
    ind = ind - width
    all = [wd, dbpedia, yago, linked, mb]
    for a in all:
        ax.bar(ind, a, width=width, align='center')
        ind = ind + width
    ax.autoscale(tight=True)
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(keys)
    plt.show()


wd_lang = get_language_share(wikidata_rdfmt)
dbpedia_lang = get_language_share(dbpedia_rdfmt)
yago_lang = get_language_share(yago_rdfmt)
linked_lang = get_language_share(linkedmdb_rdfmt)
mb_lang = get_language_share(musicbrainz_rdfmt)


# working with median!
wd_avg, wd_mean = get_all_mts(wikidata_rdfmt)
dbpedia_avg, dbpedia_mean = get_all_mts(dbpedia_rdfmt)
yago_avg, yago_mean = get_all_mts(yago_rdfmt)
linked_avg, linked_mean = get_all_mts(linkedmdb_rdfmt)
mb_avg, mb_mean = get_all_mts(musicbrainz_rdfmt)

keys = wd_avg.keys()


wd_sizes = []
dbpedia_sizes = []
yago_sizes = []
linked_sizes = []
mb_sizes = []
keys_sizes = []

wd_other = []
dbpedia_other = []
yago_other =[]
linked_other = []
mb_other = []
keys_other = []

for k in keys:
    if 'size' in k:
        wd_sizes.append(wd_mean[k])
        dbpedia_sizes.append(dbpedia_mean[k])
        yago_sizes.append(yago_mean[k])
        linked_sizes.append(linked_mean[k])
        mb_sizes.append(mb_mean[k])
        keys_sizes.append(k)
    else:
        wd_other.append(wd_mean[k])
        if k in dbpedia_mean:
            dbpedia_other.append(dbpedia_mean[k])
        else:
            dbpedia_other.append(0)
        if k in yago_mean:
            yago_other.append(yago_mean[k])
        else:
            yago_other.append(0)
        if k in linked_mean:
            linked_other.append(linked_mean[k])
        else:
            linked_other.append(0)
        if k in mb_mean:
            mb_other.append(mb_mean[k])
        else:
            mb_other.append(0)
        keys_other.append(k)


data = {'wikidata': wd_sizes, 'DBpedia': dbpedia_sizes, 'YAGO': yago_sizes, 'MusicBrainz': mb_sizes}
df = pd.DataFrame.from_dict(data)


def get_average_data(mts):
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


query_ids = json.load(open('../data/query-ids.json'))
classes = json.load(open('../data/classes.json'))
kgs = {'wikidata': wikidata_rdfmt, 'DBpedia': dbpedia_rdfmt, 'YAGO': yago_rdfmt, 'linkedmdb': linkedmdb_rdfmt, 'MusicBrainz': musicbrainz_rdfmt}

# df = pd.DataFrame(writedata)
# df.to_csv(writedata)

results = {}
for q in query_ids:
    results[q] = {}
    for kgname, rdfmt in kgs.iteritems():
        results[q][kgname] = []
        if not str(q) in classes[kgname]:
            continue
        cls = set(classes[kgname][str(q)])
        mts = []
        for c in cls:
            if kgname == 'YAGO':
                c = c.replace('http://yago-knowledge.org/resource/', '')
            elif 'http' not in c:
                continue
            if c not in rdfmt:
                #print kgname, cls
                continue
            mts.append(rdfmt[c])
        if len(mts) > 1:
            results[q][kgname] = get_average_data(mts)
        elif len(mts) == 1:
            results[q][kgname] = mts[0]




