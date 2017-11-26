import numpy as np
import csv

"""
Class to return a count of unique URIS in the datadump
"""
class UniqueURIs:

    def getUniqueSubject(self, data):
        uris = []
        for line in data:
            s = line.split('\t')[0].strip()
            if s not in uris:
                uris.append(s)
        return uris

    def getUniqueAll(self, data):
        uris = []
        for line in data:
            tmp = line.split('\t')
            if tmp[0] not in uris:
                uris.append(tmp[0])
            if tmp[1] not in uris:
                uris.append(tmp[1])
            if tmp[2] not in uris:
                uris.append(tmp[2])
        return uris

    def getUniqueNumber(self, urisList):
        return len(urisList)

"""
Class to evaluate the completeness of labels in a given dataset
"""
class CompletenessEvaluator:

    def run(self, dataPath, labelingPropertiesPath):
        labelingProperties = self.getProperties(labelingPropertiesPath)
        numberLabels = self.getLabeledURIs(dataPath, labelingProperties)
        return len(numberLabels)

    def getLabeledURIs(self, datapath, labelingProperties):
        uris = []
        with open(datapath) as data:
            for line in data:
                tmp = line.split('\t')
                if tmp[1].strip() in labelingProperties:
                    if tmp[0].strip() not in uris:
                        uris.append(tmp[0].strip())
        return uris


    def getProperties(self, labelingPropertiesPath):
        properties = []
        with open(labelingPropertiesPath) as csvFile:
            reader = csv.reader(csvFile)
            properties = reader.next()[0].split('\t')
        return properties


class EfficientAccessibilityEvaluator:
    def run(self):
        return None