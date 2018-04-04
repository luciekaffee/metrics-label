import hashlib

class Completeness:
    """ Class to measure completeness of a dataset
    """

    def __init__(self, file, labelproperties, encodeData=False, seperator='\t'):
        """
        :param file: Filename of the file investigated
        :param labelproperties: filename of the file with labeling properties
        :param encodeData: whether the data incoming is encoded with haslib.sha256, default False
        """
        self.file = file
        self.labelprop = labelproperties
        self.encodeData = encodeData
        self.seperator = seperator


    def getAllProperties(self):
        """ Helper function to get all properties in the dataset
        :return: dict with properties as key and empty [] values
        """
        unique_propertes = {}
        with open(self.file) as infile:
            for line in infile:
                pred = line.split(self.seperator)[1].strip()
                if self.encodeData:
                    pred = int(pred)
                unique_propertes[pred] = []
        return unique_propertes

    def encode(self, s):
        """ Helper function to encode strings to SHA256 integer
        :param s: string to encode
        :return: int of encoded string
        """
        if self.encodeData == True:
            return int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16)
        else:
            return s

    def getLabelingProperties(self):
        """ Helper function to get labeling properties
        :return: dict with labeling properties as key and empty [] values
        """
        properties = []
        with open(self.labelprop) as prop:
            for line in prop:
                properties.append(self.encode(line.strip()))
        return properties

    ## todo: exclude external schemas
    def getNumbersPredicate(self, labeling_properties):
        """ Get the results for predicates
        :param labeling_properties: dict, result of getLabelingProperties()
        :return: list of number of (0) unique properties and (1) unique labeled properties
        """
        unique_properties = self.getAllProperties()
        labeled = {}
        with open(self.file) as infile:
            for line in infile:
                sub = line.split(self.seperator)[0].strip()
                pred = line.split(self.seperator)[1].strip()
                if self.encodeData:
                    sub = int(sub)
                    pred = int(pred)
                if sub in unique_properties:
                    if pred in labeling_properties:
                        labeled[sub] = []
        return [len(unique_properties), len(labeled)]

    ## todo: Possibly needed to not do them at once because double the memory wasted
    def getNumbersSubjects(self, labeling_properties):
        """ Get the results for subjects
        :param labeling_properties: dict, result of getLabelingProperties()
        :return: list of number of (0) unique subjects and (1) unique labeled subjects
        """
        unique_sub = {}
        labeled = {}
        with open(self.file) as infile:
            for line in infile:
                sub = line.split(self.seperator)[0].strip()
                pred = line.split(self.seperator)[1].strip()
                if self.encodeData:
                    sub = int(sub)
                    pred = int(pred)
                unique_sub[sub] = []
                if pred in labeling_properties:
                    labeled[sub] = []
        return [len(unique_sub), len(labeled)]


    def run(self):
        """ Run function, calling above completeness metrics
        :return:
        """
        properties = self.getLabelingProperties()
        numbers_sub = self.getNumbersSubjects(properties)
        print "Unique Subjects: " + str(numbers_sub[0])
        print "Labeled Subjects: " + str(numbers_sub[1])
        numbers_pred = self.getNumbersPredicate(properties)
        print "Unique Properties: " + str(numbers_pred[0])
        print "Labeled Properties: " + str(numbers_pred[1])


class EfficientAccessibility:

    def __init__(self, file, labelproperties, encodeData=False, seperator='\t'):
        """
        :param file: Filename of the file investigated
        :param labelproperties: filename of the file with labeling properties
        :param encodeData: whether the data incoming is encoded with haslib.sha256, default False
        """
        self.file = file
        self.labelprop = labelproperties
        self.encodeData = encodeData
        self.seperator = seperator

    def getLabelingProperties(self):
        """ Helper function to get labeling properties
        :return: dict with labeling properties as key and empty [] values
        """
        properties = []
        with open(self.labelprop) as prop:
            for line in prop:
                properties.append(self.encode(line.strip()))
        return properties

    def encode(self, s):
        """ Helper function to encode strings to SHA256 integer
        :param s: string to encode
        :return: int of encoded string
        """
        if self.encodeData == True:
            return int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16)
        else:
            return s

    def getGraphs(self):
        graphs = {}
        with open(self.file) as infile:
            for line in infile:
                graph = line.split(self.seperator)[-1].strip()
                if self.encodeData:
                    graph = int(graph)
                graphs[graph] = []
        return graphs

    def getUniquePerGraph(self):
        graphs = {}
        with open(self.file) as infile:
            for line in infile:
                graph = line.split(self.seperator)[-1].strip()
                if self.encodeData:
                    graph = int(graph)
                if graph in graphs:
                    graphs[graph] +=1
                else:
                    graphs[graph] = 1
        return graphs

    def getLabeledinGraph(self, graphs, labeling_properties):
        labeled = {}
        for graph, _ in graphs.iteritems():
            tmp = {}
            with open(self.file) as infile:
                for line in infile:
                    tmp = line.split(self.seperator)
                    sub = tmp[0].strip()
                    prop = tmp[1].strip()
                    g = tmp[-1].strip()
                    if self.encodeData:
                        sub = int(sub)
                        prop = int(prop)
                        g = int(g)
                    if graph == g:
                        if prop in labeling_properties:
                            tmp[sub] = []
            labeled[graph] = len(tmp)
        return labeled

    def run(self):
        properties = self.getLabelingProperties()
        graphs = self.getGraphs()
        unique = self.getUniquePerGraph()
        labeled = self.getLabeledinGraph(graphs, properties)
        for graph in graphs:
            print "Unique: " + str(unique[graph])
            print "Labeled: " + str(labeled[graph])
        print "All Unique: " + str(sum(unique.values()))
        print "Number Graphs: " + str(len(graphs))

class Unambiguity:
    def __init__(self, file, labelproperties, encodeData=False, seperator='\t'):
        """
        :param file: Filename of the file investigated
        :param labelproperties: filename of the file with labeling properties
        :param encodeData: whether the data incoming is encoded with haslib.sha256, default False
        """
        self.file = file
        self.labelprop = labelproperties
        self.encodeData = encodeData
        self.seperator = seperator

    def encode(self, s):
        """ Helper function to encode strings to SHA256 integer
        :param s: string to encode
        :return: int of encoded string
        """
        if self.encodeData == True:
            return int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16)
        else:
            return s

    def getLabelingProperties(self):
        """ Helper function to get labeling properties
        :return: dict with labeling properties as key and empty [] values
        """
        properties = []
        with open(self.labelprop) as prop:
            for line in prop:
                properties.append(self.encode(line.strip()))
        return properties

    def getSubjects(self):
        subjects = set()
        counter_ambig = 0
        properties = self.getLabelingProperties()
        with open(self.file) as infile:
            for line in infile:
                tmp = line.split(self.seperator)
                sub = tmp[0].strip()
                pred = tmp[1].strip
                if self.encodeData:
                    sub = int(sub)
                    pred = int(pred)
                if len(tmp) < 2:
                    continue
                if pred in properties:
                    if sub in subjects:
                        counter_ambig += 1
                    else:
                        subjects.add(sub)
        return counter_ambig

    def run(self):
        number_ambig = self.getSubjects()
        print "number ambigious entities: " + str(number_ambig)


