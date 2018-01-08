import bz2

bz_file = bz2.BZ2File('latest-truthy.nt.bz2', 'r')

label_c = 0
altLabel_c = 0
descr_c = 0
has_labels_dict = {}
counter = 0
#objects = {}
for line in bz_file:
    if "schema.org/name" in line or "skos/core#altLabel" in line or "schema.org/description" in line:
        item = line.split()[0].replace('<http://www.wikidata.org/entity/', '')
        has_labels_dict[item] = {}
        if "schema.org/name" in line:
            label_c += 1
        elif "skos/core#altLabel" in line:
            altLabel_c += 1
        elif "schema.org/description" in line:
            descr_c += 1
        counter += 1


print "number label properties: " + str(label_c)
print "number altLabel properties: " + str(altLabel_c)
print "number description properties: " + str(descr_c)

print "Number of items with labels: " + str(len(has_labels_dict.keys()))


