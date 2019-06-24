import json
import os
import tarfile


class BasicRDFMTCreator():

    def create_file(self, kgname, rdfmt):
        with open('data/' + kgname + '-basic' + '.json', 'w') as outfile:
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
                    mtclass = f.replace('.json', '').replace('.txt', '').replace('_', '/').replace('-', ':')
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
            #self.create_file(kgname, rdfmt)
            all.append(rdfmt)
        return all


class BasicRDFMTCleaner():

    def create_file(self, kgname, rdfmt):
        with open('data/' + kgname + '-rdfmt-raw' + '.json', 'w') as outfile:
            json.dump(rdfmt, outfile)

    def run(self, kgdata):
        allrdfmt = []
        for kg in kgdata:
            rdfmt = {}
            for kgname, data in kg.iteritems():
                print kgname
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
                        #elif kgname == 'wikidata':
                        #    rdfmt[kgname][mtclass][q] = r[0]
                        elif q == 'Q10':
                            #tmp = {}
                            #for x in r:
                            #    tmp[x['lt']] = x['count']
                            #rdfmt[kgname][mtclass][q] = tmp
                            rdfmt[kgname][mtclass][q] = r[0]
                        #elif q == 'Q11':
                        #    rdfmt[kgname][mtclass][q] = r[0]['callret-0']
                        #else:
                        #    rdfmt[kgname][mtclass][q] = r[0]['count']
                        else:
                            rdfmt[kgname][mtclass][q] = int(r[0])
            #self.create_file(kgname, rdfmt)
            allrdfmt.append(rdfmt)
        return allrdfmt



class RDFMTAdder():

    def create_file(self, kgname, rdfmt):
        with open('data/rdfmt/' + kgname + '-rdfmt' + '.json', 'w') as outfile:
            json.dump(rdfmt, outfile)

    def create_rdfmt_content(self, data):
        content = {}
        if 'Q1' in data and data['Q1']:
            content['ds_size_triples'] = float(data['Q1'])
        else:
            content['ds_size_triples'] = []
        #if 'Q2' in data and data['Q2']:
        #    content['ds_subproperty_usage'] = float(data['Q2'])
        #else:
        #    content['ds_subproperty_usage'] = []
        if 'Q3' in data and 'Q4' in data and data['Q3'] and data['Q4']:
            content['ds_class_labeling'] = float(data['Q3'])/float(data['Q4'])
        else:
            content['ds_class_labeling'] = []
        #if 'Q6' in data and 'Q5' in data and data['Q6'] and data['Q5']:
        #    content['ds_property_labeling'] = float(data['Q6']) / float(data['Q5'])
        #else:
        #    content['ds_property_labeling'] = []
        if 'Q7' in data and  data['Q7']:
            content['size_triples'] = float(data['Q7'])
        else:
            content['size_triples'] = []
        if 'Q11' in data and data['Q11']:
            content['number_languages'] = float(data['Q11'])
        else:
            content['number_languages'] = []

        if 'Q8' in data and data['Q8'] and float(data['Q8']) <= 0:
            return content

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


    def run(self, kgdata):
        results = {}
        for kg in kgdata:
            rdfmt = {}
            for kgname, data in kg.iteritems():
                print kgname
                rdfmt[kgname] = {}
                for mtclass, results in data.iteritems():
                    content = self.create_rdfmt_content(results)
                    rdfmt[kgname][mtclass] = content
                self.create_file(kgname, rdfmt)
                results[kgname] = rdfmt
        return results

















