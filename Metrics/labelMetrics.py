import hashlib

class Completeness:
    """ Class to measure completeness of a dataset
    """

    def __init__(self, file, labelproperties):
        """
        :param file: Filename of the file investigated
        :param labelproperties: filename of the file with labeling properties
        """
        self.file = file
        self.labelprop = labelproperties


    def getAllProperties(self):
        """ Helper function to get all properties in the dataset
        :return: dict with properties as key and empty [] values
        """
        unique_propertes = {}
        with open(self.file) as infile:
            for line in infile:
                pred = int(line.split('\t')[1].strip())
                unique_propertes[pred] = []
        return unique_propertes

    def encode(self, s):
        """ Helper function to encode strings to SHA256 integer
        :param s: string to encode
        :return: int of encoded string
        """
        return int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16)
        #return id(s)

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
                sub = int(line.split('\t')[0].strip())
                if sub in unique_properties:
                    if int(line.split('\t')[1].strip()) in labeling_properties:
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
                sub = int(line.split('\t')[0].strip())
                unique_sub[sub] = []
                if int(line.split('\t')[1].strip()) in labeling_properties:
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

    def __init__(self, file, labelproperties):
        """
        :param file: Filename of the file investigated
        :param labelproperties: filename of the file with labeling properties
        """
        self.file = file
        self.labelprop = labelproperties

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
        return int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16)
        #return id(s)

    def getGraphs(self):
        graphs = {}
        with open(self.file) as infile:
            for line in infile:
                graph = int(line.split('\t')[-1].strip())
                graphs[graph] = []
        return graphs

    def getUniquePerGraph(self):
        graphs = {}
        with open(self.file) as infile:
            for line in infile:
                graph = int(line.split('\t')[-1].strip())
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
                    if graph == int(line.split('\t')[-1].strip()):
                        if int(line.split('\t')[1].strip()) in labeling_properties:
                            tmp[int(line.split('\t')[0].strip())] = []
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

