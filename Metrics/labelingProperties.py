import json

class LabelingPropertiesExtractor:
    """ Class to extract labeling properties
    """

    def __init__(self, infile, outfile):
        self.infile = infile
        self.outfile = outfile

    def _isnumber(self, s):
        """ Function to test if a string is a number
        :param s: string to test
        :return: Boolean if the
        """
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass

        return False

    def _getpropertiescounted(self):
        properties = {}
        with open(self.infile) as infile:
            for line in infile:
                tmp = line.split(' ')
                if len(tmp) < 2:
                    continue
                if tmp[2].strip().startswith('"') and not self._isnumber(tmp[2].strip().replace('"', '')):
                    if tmp[1].strip() in properties:
                        properties[tmp[1].strip()] += 1
                    else:
                        properties[tmp[1].strip()] = 0
        return properties

    def run(self):
        properties = self._getpropertiescounted()
        with open(self.outfile+'-counted', 'w') as outfile:
            for k,v in properties.iteritems():
                outfile.write(k + '\t' + str(v) + '\n')
        with open(self.outfile, 'w') as outfile:
            for k, v in properties.iteritems:
                outfile.write(k + '\n')
