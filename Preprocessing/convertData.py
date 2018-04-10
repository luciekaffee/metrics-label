import gzip
import os
import hashlib


class ConvertData():
    def __init__(self, outfile, filename='', directory=''):
        self.infile = filename
        self.outfile = outfile
        self.directory = directory

    def encode(self, s):
        return int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16)

    # int( hashlib.sha256(s.encode('utf-8'd)).hexdigest(), 16 )
    def convert(self, line):
        triple = line.strip().split(' ')
        sub = triple[0]
        pred = triple[1]
        if len(triple) > 3 and 'http' in triple[-2]:
            obj = " ".join(triple[2:-2])
            graph = triple[-2]
        else:
            obj = " ".join(triple[2:])

        result = str(self.encode(sub)) + '\t' + str(self.encode(pred)) + '\t' + str(self.encode(obj))
        if graph:
            result += '\t' + str(self.encode(graph))

        return result

    #todo: out needs to be compressed file, too
    def run_compressed(self):
        with open(self.outfile, 'w') as out:
            for filename in os.listdir(self.directory):
                if filename.endswith(".gz") and filename.startswith('btc'):
                    print filename
                    with gzip.open(self.directory + '/' + filename) as infile:
                        for line in infile:
                            out.write(self.convert(line) + '\n')

    def run_2014(self):
        with gzip.open(self.outfile, 'wb') as out:
            for i in range(1, 14):
                dir = self.directory + str(i).zfill(2) + '/'
                for filename in os.listdir(dir):
                    if filename.startswith('data.nq') and filename.endswith('.gz'):
                        filepath = os.path.join(dir, filename)
                        print 'Processing file ' + filename + ' from directory ' + str(i)
                        file = gzip.open(filepath)
                        for line in file:
                            out.write(self.convert(line) + '\n')


    def run(self):
        with open(self.outfile, 'w') as out:
            with open(self.infile) as infile:
                for line in infile:
                    if len(line.strip().split(' ')) > 2:
                        out.write(self.convert(line) + '\n')

