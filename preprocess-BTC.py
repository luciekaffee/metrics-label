import os
import gzip

"""
Class to preprocess BTC 2010 dump
"""
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

"""
Class to preprocess BTC 2014 dump
"""
class Preprocessing_BTC_2014:
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
        for i in range(1,14)
            counter = 0
            while True:
                file = self.folder + str().zfill(3) 'btc-2010-chunk-' + str(counter).zfill(2) + '.gz'
                if not os.path.exists(file):
                    break
                print 'Processing file btc-2010-chunk-' + str(counter).zfill(2) + '.gz'
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



"""
Call class and run it
"""
pre_btc_2014 = Preprocessing_BTC_2014('../btc-2014/projects/btc-2014/data/crawls', 'data/btc-2014.csv')

pre_btc_2014.run()
pre_btc_2014.limit('../btc-2014/projects/btc-2014/data/redirects.nx.gz', 'data/nir-btc-2014.csv')

#pre_btc_2010 = Preprocessing_BTC_2010('../btc-2010/', 'data/btc-2010.csv')

#pre_btc_2010.run()
#pre_btc_2010.limit('../btc-2010/redirects.nx.gz', 'data/nir-btc-2010.csv')
