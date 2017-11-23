import os
import gzip


class Preprocessing_BTC_2010:
    def __init__(self, nirpath, folder, outfile):
        self.folder = folder
        self.out = outfile
        self.nir = self.getNIRS(nirpath)

    def process_file(self, filepath):
        file = gzip.open(filepath)
        for line in file:
            with open(self.out, 'a+') as out:
                triple = line.split()[:-2]
                s = triple[0].strip()
                p = triple[1].strip()
                o = ' '.join(triple[2:]).strip()
                if s in self.nir:
                    out.write(s + '\t' + p + '\t' + o + '\n')

    def run(self):
        counter = 0
        while True:
            file = self.folder + 'btc-2010-chunk-' + str(counter).zfill(3) + '.gz'
            if not os.path.exists(file):
                break
            print 'Processing file btc-2010-chunk-' + str(counter).zfill(3) + '.gz'
            self.process_file(file)
            counter += 1

    def getNIRS(self, nirpath):
        nirs = []
        with gzip.open(nirpath) as infile:
            for line in infile:
                nirs.append(line.split()[0].strip())
        return nirs
