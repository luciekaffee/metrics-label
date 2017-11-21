import os
import gzip


class Preprocessing_BTC_2010:
    def __init__(self, folder, outfile):
        self.folder = folder
        self.out = outfile

    def process_file(self, filepath):
        file = gzip.open(filepath)
        for line in file:
            with open(self.out, 'a+') as out:
                triple = line.split()[:-2]
                s = triple[0]
                p = triple[1]
                o = ' '.join(triple[2:])
                out.write(s + '\t' + p + '\t' + o + '\n')

    def run(self):
        counter = 000
        while True:
            file = self.folder + 'btc-2010-chunk-' + str(counter).zfill(3) + '.gz'
            if not os.path.exists(file):
                break
            print 'Processing file btc-2010-chunk-' + str(counter).zfill(3) + '.gz'
            self.process_file(file)
            counter += 1