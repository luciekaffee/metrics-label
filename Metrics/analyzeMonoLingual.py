import gzip
import json

class AnalyzeMonoLingualIslands():
    def __init__(self, infile, outfile):
        self.infile = infile
        self.outfile = outfile

    def getCodes(self):
        codes = set()
        data = json.load(open('language-codes.json'))
        for d in data:
            codes.add(d['code'])
        return codes

    def getData(self):
        data = {}
        codes = self.getCodes()
        if self.infile.endswith('.gz'):
            file = gzip.open(self.infile)
        else:
            file = open(self.infile)

        for line in file:
            nrlangs = 0
            langs = line.replace('set(', '').replace(')', '').replace('[','').replace(']', '').replace("'", '').split('\t')[1].split(',')
            for lang in langs:
                if lang.strip() in codes:
                    nrlangs += 1

            if nrlangs in data:
                data[nrlangs] += 1
            else:
                data[nrlangs] = 1
        return data

    def run(self):
        data = self.getData()
        with open(self.outfile, 'w') as out:
            for k,v in data.iteritems():
                out.write(str(k) + '\t' + str(v) + '\n')