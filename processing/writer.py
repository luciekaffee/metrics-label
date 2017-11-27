import csv

"""
Class to write Dictonary to a file
"""
class DictWriter():
    def write(self, outfile, data):
        with open(outfile, 'w') as out:
            w = csv.DictWriter(out, data.keys(), delimiter='\t')
            w.writeheader()
            w.writerow(data)
