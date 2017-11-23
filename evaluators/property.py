import re
from dateutil.parser import parse

"""
Class to get the properties used for labeling
"""
class LabelingProperties:
#    def __init__(self)

    def run(self, data):
        labeling_properties = self.analyze(data)
        return labeling_properties


    def analyze(self, data):
        labeling_properties = {}

        with open(data) as infile:
            for line in infile:
                tmp = line.split('\t')

                # check if string is number
                if tmp[2].strip().replace('"').isdigit():
                    continue

                pattern = re.compile("<.*>")
                # use all datatype string
                if '^^<http://www.w3.org/2001/XMLSchema#string>' in tmp[2] and not not pattern.match(tmp[2]):
                    if not tmp[1] in labeling_properties:
                        labeling_properties[tmp[1]] = 1
                    else:
                        labeling_properties[tmp[1]] += 1

                if not pattern.match(tmp[2]) and not 'XMLSchema' in tmp[2]:
                    if not tmp[1] in labeling_properties:
                        labeling_properties[tmp[1]] = 1
                    else:
                        labeling_properties[tmp[1]] += 1

        return labeling_properties


    def is_date(string):
        try:
            parse(string)
            return True
        except ValueError:
            return False

    """
    limits a dictornary to all entries with a value of at least 10.000
    """
    def limit(self, data):
        delete = []
        for k,v in data.iteritems():
            if v <= 10000:
                delete.append(k)
        for d in delete:
            del data[d]
        return data
