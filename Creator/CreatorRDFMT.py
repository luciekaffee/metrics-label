import json
import os
import tarfile


class BasicRDFMTCreator():

    def create_file(self, kgname, rdfmt):
        with open(kgname + '-basic' + '.json', 'w') as outfile:
            json.dump(rdfmt, outfile)

    def run(self, directory):
        all = []
        for dirname in os.listdir(directory):
            if 'tar.gz' in dirname:
                continue
            rdfmt = {}
            kgname = dirname
            rdfmt[kgname] = {}
            for querydir in os.listdir(directory + '/' + dirname):
                query = querydir
                for f in os.listdir(directory + '/' + dirname + '/' + querydir):
                    mtclass = f.replace('.json', '').replace('_', '/').replace('-', ':')
                    with open(directory + '/' + dirname + '/' + querydir + '/' + f) as infile:
                        content = json.load(infile)
                        if int(query.replace('Q', '')) < 7:
                            if 'all' in rdfmt[kgname]:
                                rdfmt[kgname]['all'][query] = content
                            else:
                                rdfmt[kgname]['all'] = {}
                                rdfmt[kgname]['all'][query] = content
                        else:
                            if mtclass in rdfmt[kgname]:
                                rdfmt[kgname][mtclass][query] = content
                            else:
                                rdfmt[kgname][mtclass] = {}
                                rdfmt[kgname][mtclass][query] = content
            self.create_file(kgname, rdfmt)
            all.append(rdfmt)
        return all


class BasicRDFMTCleaner():

    def create_file(self, kgname, rdfmt):
        with open(kgname + '-rdfmt-clean' + '.json', 'w') as outfile:
            json.dump(rdfmt, outfile)

    def run(self, kgdata):
        for kg in kgdata:
            rdfmt = {}
            for kgname, data in kg.iteritems():
                rdfmt[kgname] = {}
                all = data['all']
                for mtclass, results in data.iteritems():
                    if mtclass == 'all':
                        continue
                    rdfmt[kgname][mtclass] = {}

                    # add the general dataset statistics to each RDF MT
                    for q,r in all.iteritems():
                        if not r:
                            rdfmt[kgname][mtclass][q] = []
                        else:
                            rdfmt[kgname][mtclass][q] = r[0]['count']

                    # clean each result for all queries for all RDF MT
                    for q, r in results.iteritems():
                        if not r:
                            rdfmt[kgname][mtclass][q] = []
                        elif q == 'Q10':
                            tmp = {}
                            for x in r:
                                tmp[x['lt']] = x['count']
                            rdfmt[kgname][mtclass][q] = tmp
                        elif q == 'Q11':
                            rdfmt[kgname][mtclass][q] = r[0]['callret-0']
                        else:
                            rdfmt[kgname][mtclass][q] = r[0]['count']
            self.create_file(kgname, rdfmt)







#class RDFMTAdder():













