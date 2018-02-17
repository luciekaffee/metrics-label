import hashlib

class Completeness:

    def __init__(self, file, labelproperties):
        self.file = file
        self.labelprop = labelproperties

    ## Possibly needed to not do them at once because double the memory wasted
    def getNumbersSubjects(self, properties):
        unique_sub = {}
        labeled = {}
        with open(self.file) as infile:
            for line in infile:
                sub = int(line.split('\t')[0].strip())
                unique_sub[sub] = []
                if int(line.split('\t')[1].strip()) in properties:
                    labeled[sub] = []
        return [len(unique_sub), len(labeled)]

    def encode(self, s):
        return int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16)
        #return id(s)

    def getProperties(self):
        properties = []
        with open(self.labelprop) as prop:
            for line in prop:
                properties.append(self.encode(line.strip()))
        return properties


    def run(self):
        properties = self.getProperties()
        numbers = self.getNumbersSubjects(properties)
        print "Unique Subjects:" + str(numbers[0])
        print "Labeled Subjects:" + str(numbers[1])

