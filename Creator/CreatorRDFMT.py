import json
import os
import tarfile


class BasicRDFMTCreator():

    def create_file(self, kgname, rdfmt):
        with open(kgname + '-basic' + '.json', 'w') as outfile:
            json.dump(rdfmt, outfile)

    def run(self, directory):
        for filename in os.listdir('../Metrics_Results'):
            rdfmt = {}
            kgname = filename.replace('.tar.gz', '')
            tar = tarfile.open(filename)
            for member in tar.getmembers():
                f = tar.extractfile(member)
                content = f.read()
                tmp = member.name.split('/')
                query = tmp[1]
                mtclass = tmp[2]
                rdfmt[mtclass][query] = content
        self.create_file(kgname, rdfmt)



