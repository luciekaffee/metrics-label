import json
import os
import tarfile

class RDFMTMerger():

    def create_file(self, rdfmt):
        with open('data/mergerresult.json', 'w') as outfile:
            json.dump(rdfmt, outfile)

    def create_Q10(self, qid, k, v, data):
        val = {}
        for t in v:
            val[t.keys()[0]] = t.values()[0]
        if k in data[qid]:
            tmp_val = {}
            for t in data[qid][k]:
                tmp_val[t.keys()[0]] = t.values()[0]
            return {key: tmp_val.get(key, 0) + val.get(key, 0) for key in set(tmp_val) | set(val)}
        else:
            return val

    def run(self):
        data = {}
        for dirname in os.listdir('data/raw'):
            for x in range(1, 18):
                qid = 'Q' + x
                with open('data/raw' + dirname + '/Q' + x + '.json') as infile:
                    tmp = json.load(infile)
                    if x < 7:
                        if qid in data:
                            data[qid] += tmp[0]['callret-0']['value']
                        else:
                           data[qid] = tmp[0]['callret-0']['value'] 
                    elif x == 10:
                        if qid not in data:
                            data[qid] = {}
                        for k, v in tmp:
                            data[qid][k] = self.create_Q10(qid, k, v, data)

                    else:
                        if qid not in data:
                            data[qid] = {}
                        for k,v in tmp:
                            if k in data[qid]:
                                data[qid][k] += int(v[0])
                            else:
                                data[qid][k] = int(v[0])
        self.create_file(data)
        return data





class BasicRDFMTCreator():

    def create_file(self, rdfmt):
        with open('data/rdfmt-raw.json', 'w') as outfile:
            json.dump(rdfmt, outfile)

    def get_classes(self, data):
        classes = set()
        for k, v in data:
            classes.update(v.keys())
        return classes

    def run(self, data):
        rdfmt_raw = {}
        classes = self.get_classes(data)
        for c in classes:
            rdfmt_raw[c] = {}
            for x in range(1, 18):
                qid = 'Q' + x
                if x < 7:
                    rdfmt_raw[c][qid] = data[qid]
                else:
                    rdfmt_raw[c][qid] = data[qid][c]
        self.create_file(rdfmt_raw)
        return rdfmt_raw


class RDFMTAdder():

    def create_file(self, rdfmt):
        with open('data/rdfmt.json', 'w') as outfile:
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


    def run(self, rdfmt_raw):
        rdfmt = {}
        for mtclass, results in rdfmt_raw.iteritems():
            content = self.create_rdfmt_content(results)
            rdfmt[mtclass] = content
        self.create_file(rdfmt)
        return rdfmt

















