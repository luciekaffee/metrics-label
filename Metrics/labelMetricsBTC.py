import gzip
import os

class BTC14:
    def __init__(self, directory, langsoutfile, monolingoutfile):
        self.directory = directory
        self.langsoutfile = langsoutfile
        self.monolingoutfile = monolingoutfile

    def getlanguages(self, line, langs, monoling):
        """"
        :return: dict with language and how often they occur
        """
        if '@' in line:
            line = line.replace('.', '').strip()
            value = line.split(' ')[-2]
            subject = line.split(' ')[0]
            if '@' in value:
                lang = value.split('@')[1].strip()
                if '"' not in lang and not lang.endswith('>') and len(lang) < 5:
                    if lang in langs:
                        langs[lang] += 1
                    else:
                        langs[lang] = 1
                    if lang not in monoling:
                        monoling[subject] = [lang]
                    else:
                        monoling[subject].append(lang)
        return [langs, monoling]

    def run(self):
        langs = {}
        monoling = {}

        # 14 folders with data (1 - 14)
        for i in range(1, 15):
            dir = self.directory + str(i).zfill(2) + '/'
            for filename in os.listdir(dir):
                if filename.startswith('data.nq') and filename.endswith('.gz'):
                    filepath = os.path.join(dir, filename)
                    print 'Processing file ' + filename + ' from directory ' + str(i)
                    file = gzip.open(filepath)
                    for line in file:
                        data = self.getlanguages(line, langs, monoling)
                        langs = data[0]
                        monoling = data[1]
        print 'all files processed'

        with gzip.open(self.monolingoutfile, 'wb') as outmono:
            with gzip.open(self.langsoutfile, 'wb') as out:
                print 'write to files'
                for k, v in langs.iteritems():
                    out.write(k + '\t' + str(v) + '\n')
                print 'finished language file'
                for k, v in monoling.iteritems():
                    outmono.write(k + '\t' + str(v) + '\n')
                print 'finished monoling file'

class BTC10:
    def __init__(self, directory, langsoutfile):
        self.directory = directory
        self.langsoutfile = langsoutfile

    def getlanguages(self, line, monoling):
        """"
        :return: dict with language and how often they occur
        """
        if '@' in line:
            line = line.replace('.', '').strip()
            value = line.split(' ')[-2]
            subject = line.split(' ')[0]
            if '@' in value:
                lang = value.split('@')[1].strip()
                if '"' not in lang:
                    if lang not in monoling:
                        monoling[subject] = [lang]
                    else:
                        monoling[subject].append(lang)
        return monoling

    def run(self):
        monoling = {}
        for filename in os.listdir(self.directory):
            if filename.endswith(".gz") and filename.startswith('btc'):
                print filename
                with gzip.open(self.directory + '/' + filename) as infile:
                    for line in infile:
                        monoling = self.getlanguages(line, monoling)

        with open(self.langsoutfile, 'w') as out:
            for k, v in langs.iteritems():
                #print k + '\t' + str(v) + '\n'
                out.write(k + '\t' + str(v) + '\n')