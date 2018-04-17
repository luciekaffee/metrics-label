import gzip

class AnalyzeMonoLingualIslands():
    def __init__(self, infile, outfile):
        self.infile = infile

    def getData(self):
        data = {}
        if self.infile.endswith('.gz'):
            file = gzip.open(self.infile)
        else:
            file = open(self.infile)

        for line in file:
            nrlangs = len(line.split('\t')[1].split(','))

            if nrlangs in data:
                data[nrlangs] += 1
            else:
                data[nrlangs] = 1
        return data

    def run(self):
        data = self.getData()
        with open(self.outfile, 'w') as out:
            for k,v in data.iteritems():
                out.write(k + '\t' + v)