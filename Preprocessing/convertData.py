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
        obj = " ".join(triple[2:-2])
        graph = triple[-2]
        return str(self.encode(sub)) + '\t' + str(self.encode(pred)) + '\t' + str(self.encode(obj)) + '\t' + str(self.encode(graph))

    def run_compressed(self):
        with open(self.outfile, 'w')as out:
            for filename in os.listdir(self.directory):
                if filename.endswith(".gz") and filename.startswith('btc'):
                    print filename
                    with gzip.open(self.directory + '/' + filename) as infile:
                        for line in infile:
                            out.write(self.convert(line) + '\n')

    def run(self):
        with open(self.outfile, 'w') as out:
            with open(self.infile) as infile:
                for line in infile:
                    if len(line.strip().split(' ')) > 3:
                        out.write(self.convert(line) + '\n')


