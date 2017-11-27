import os
import gzip


class Preprocessing_BTC_2010:
    def __init__(self,  folder, outfile):
        self.folder = folder
        self.out = outfile

    def process_file(self, filepath):
        file = gzip.open(filepath)
        for line in file:
            with open(self.out, 'a+') as out:
                triple = line.split()[:-2]
                s = triple[0].strip()
                p = triple[1].strip()
                o = ' '.join(triple[2:]).strip()
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

    def limit(self, nirpath, newoutfile):
        nirs = self.getNIRS(nirpath)
        newfile = open(newoutfile, 'w')
        with open(self.out) as orgfile:
            for line in orgfile:
                triple = line.strip().split('\t')
                if triple[0].strip() in nirs:
                    newfile.write(line)

    def getNIRS(self, nirpath):
        nirs = {}
        with gzip.open(nirpath) as infile:
            for line in infile:
                if ' ' in line:
                    nirs[line.split()[0].strip()] = ''
        return nirs
