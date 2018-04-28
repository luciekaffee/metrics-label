import hashlib
import numpy
import gzip

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
        if self.file.endswith('.gz'):
            infile = gzip.open(self.file)
        else:
            infile = open(self.file)
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
        if self.file.endswith('.gz'):
            infile = gzip.open(self.file)
        else:
            infile = open(self.file)
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
        if self.file.endswith('.gz'):
            infile = gzip.open(self.file)
        else:
            infile = open(self.file)
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
        if self.file.endswith('.gz'):
            infile = gzip.open(self.file)
        else:
            infile = open(self.file)
        for line in infile:
            graph = line.split(self.seperator)[-1].strip()
            if self.encodeData:
                graph = int(graph)
            graphs[graph] = []
        return graphs

    def getUniquePerGraph(self):
        graphs = {}
        if self.file.endswith('.gz'):
            infile = gzip.open(self.file)
        else:
            infile = open(self.file)
        for line in infile:
            graph = line.split(self.seperator)[-1].strip()
            subject = line.split(self.seperator)[0].strip()
            if self.encodeData:
                graph = int(graph)
                subject = int(subject)
            if graph in graphs:
                if subject not in graphs[graph]:
                    graphs[graph].append(subject)
            else:
                graphs[graph] = [subject]
        return graphs

    def getLabeledinGraph(self, graphs, labeling_properties):
        labeled = {}
        for graph, _ in graphs.iteritems():
            tmp = []
            if self.file.endswith('.gz'):
                infile = gzip.open(self.file)
            else:
                infile = open(self.file)
            for line in infile:
                trip = line.split(self.seperator)
                sub = trip[0].strip()
                prop = trip[1].strip()
                g = trip[-1].strip()
                if self.encodeData:
                    sub = int(sub)
                    prop = int(prop)
                    g = int(g)
                if graph == g:
                    if prop in labeling_properties:
                        tmp.append(sub)
            labeled[graph] = len(tmp)
        return labeled

    def run(self):
        properties = self.getLabelingProperties()
        graphs = self.getGraphs()
        unique = self.getUniquePerGraph()
        labeled = self.getLabeledinGraph(graphs, properties)
        for graph in graphs:
            print graph
            print "Unique: " + str(len(unique[graph]))
            print "Labeled: " + str(labeled[graph])
        all_uniq = 0
        for k,v in unique.iteritems():
            all_uniq += len(v)
        print "All Unique: " + str(all_uniq)
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
        ambig = set()
        properties = self.getLabelingProperties()
        if self.file.endswith('.gz'):
            infile = gzip.open(self.file)
        else:
            infile = open(self.file)
        for line in infile:
            tmp = line.split(self.seperator)
            if len(tmp) < 2:
                continue
            sub = tmp[0].strip()
            pred = tmp[1].strip()
            if self.encodeData:
                sub = int(sub)
                pred = int(pred)
            if pred in properties:
                if sub in subjects:
                    if sub not in ambig:
                        ambig.add(sub)
                else:
                    subjects.add(sub)
        return len(ambig)

    def run(self):
        number_ambig = self.getSubjects()
        print "number ambigious entities: " + str(number_ambig)

class Multilinguality:
    """
    Class to investigate the number of languages used in a dataset
    """
    def __init__(self, infile, outfile, seperator='\t'):
        """
        :param infile: Filename of the file investigated
        :param outfile: Place to write the language results
        :param seperator: Seperator used in infile
        """
        self.infile = infile
        self.outfile = outfile
        self.seperator = seperator

    def getlanguages(self):
        """"
        :return: dict with language and how often they occur
        """
        langs = {}
        if self.infile.endswith('.gz'):
            infile = gzip.open(self.infile)
        else:
            infile = open(self.infile)
        for line in infile:
            if '@' in line:
                line = line.replace('.', '').strip()
                value = line.split(self.seperator)[-1]
                if '@' in value:
                    lang = value.split('@')[1].strip()
                    if '"' not in lang:
                        if lang in langs:
                            langs[lang] += 1
                        else:
                            langs[lang] = 0
        return langs

    def run(self):
        langs = self.getlanguages()
        with open(self.outfile, 'w') as out:
            for k, v in langs.iteritems():
                out.write(k + '\t' + str(v) + '\n')

class MonolingualIsland:
    """
    Class to investigate how many entities are in one or more languages available
    """
    def __init__(self, infile, outfile, encodeData=False, seperator='\t'):
        """
        :param infile: Filename of the file investigated
        :param outfile: Place to write the language results
        :param seperator: Seperator used in infile
        """
        self.infile = infile
        self.outfile = outfile
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

    def getData(self):
        data = {}
        if self.infile.endswith('.gz'):
            infile = gzip.open(self.infile)
        else:
            infile = open(self.infile)
        for line in infile:
            if '@' in line:
                line = line.replace('.', '').strip()
                value = line.split(self.seperator)[-1]
                subject = line.split(self.seperator)[0]
                subject = self.encode(subject)
                if self.encodeData:
                    value = int(value)
                    subject = int(subject)
                if '@' in value:
                    lang = value.split('@')[1].strip()
                    if '"' not in lang:
                        if subject not in data:
                            data[subject] = [lang]
                        else:
                            data[subject].append(lang)
        return data

    def getMoreThanTwo(self, data):
        counter = 0
        for k, v in data.iteritems():
            if v >= 2:
                counter += 1
        return counter

    def run(self):
        data = self.getData()
        print 'got data'
        print 'entities in more than two languages: ' + str(self.getMoreThanTwo(data))
        with open(self.outfile, 'w') as out:
            for k, v in data.iteritems():
                out.write(k + '\t' + str(v) + '\n')

class LabelAndUsage:
    """
    This metric measures whether the higher used entities are more likely to have a label as well
    """
    def __init__(self, infile, outfile, labelproperties, encodeData=False, seperator='\t'):
        """
        :param infile: Filename of the file investigated
        :param outfile: Place to write the language results
        :param seperator: Seperator used in infile
        """
        self.infile = infile
        self.outfile = outfile
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

    def getlabelingproperties(self):
        """ Helper function to get labeling properties
        :return: dict with labeling properties as key and empty [] values
        """
        properties = set()
        with open(self.labelprop) as prop:
            for line in prop:
                properties.add(self.encode(line.strip()))
        return properties

    def getobjects(self):
        """
        get objects from a datafile
        :return: dict in the form {object: int(numberUsage)}
        """
        objects = {}
        if self.infile.endswith('.gz'):
            infile = gzip.open(self.infile)
        else:
            infile = open(self.infile)
        for line in infile:
            tmp = line.split(self.seperator)
            if len(tmp) < 3:
                continue
            object = tmp[2].strip()
            if self.encodeData:
                object = int(object)

            if not self.encodeData:
                if 'http' not in object or not object.startswith('<'):
                    continue
            if object in objects:
                objects[object] += 1
            else:
                objects[object] = 1
        return objects

    def getlabeledobjects(self, labelingproperties, objects):
        labeledobjects = {}
        if self.infile.endswith('.gz'):
            infile = gzip.open(self.infile)
        else:
            infile = open(self.infile)
        for line in infile:
            tmp = line.split(self.seperator)
            subject = tmp[0].strip()
            prop = tmp[1].strip()
            if self.encodeData:
                subject = int(subject)
                prop = int(prop)
            if subject in objects:
                if prop in labelingproperties:
                    if subject in labeledobjects:
                        labeledobjects[subject] += 1
                    else:
                        labeledobjects[subject] = 1
        return labeledobjects

    def analyzeLabeledObjects(self, objects, labeledObjects):
        """
        Check how labeled objects relate to object usage
        :param objects: dict in the form {object: int(numberUsage)}
        :param labeledObjects: list of labeled objects
        :return:
        """
        counter_labeled = []
        counter_unlabeled = []
        for ob, num in objects.iteritems():
            if ob in labeledObjects:
                counter_labeled.append(num)
            else:
                counter_unlabeled.append(num)

        print 'total average usage: ' + str(numpy.mean(objects.values()))
        print "average labeled usage: " + str(numpy.mean(counter_labeled))
        print 'average unlabeled usage: ' + str(numpy.mean(counter_unlabeled))


    def run_only_labeled(self):
        labelingProperties = self.getlabelingproperties()
        print 'LabelUsage: Got Properties'
        objects = self.getobjects()
        print 'LabelUsage: Got Objects'
        labeledObjects = self.getlabeledobjects(labelingProperties, objects)
        for obj, num in labeledObjects:
            with gzip.open(self.outfile, 'wb') as out:
                if obj not in labeledObjects:
                    continue
                out.write(obj + '\t' + num + labeledObjects[obj])
        print 'wrote to file'


    def run(self):
        labelingProperties = self.getlabelingproperties()
        print 'LabelUsage: Got Properties'
        objects = self.getobjects()
        print 'LabelUsage: Got Objects'
        labeledObjects = self.getlabeledobjects(labelingProperties, objects)
        print 'LabelUsage: Got Labeled Objects'
        self.analyzeLabeledObjects(objects, labeledObjects)
        print 'LabelUsage: Finished'
        #print objects
        #print labeledObjects
        # plot the number used that have a label vs no label
