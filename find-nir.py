import httplib

counter = 0
counter_nir = 0
labels = {}

with open('has-labels.csv') as infile:
    for line in infile:
        labels[line.replace('<','').replace('>','')] = {}


with open('obj.txt') as infile:
    for line in infile:
        url = line.replace('<','').replace('>','')
        conn = httplib.HTTPConnection("www.google.com")
        conn.request("HEAD", "/index.html")
        res = conn.getresponse()
        if res.status == 303 or res.status == 302:
            counter_nir += 1
            if url in labels:
                counter += 1

print "All NIR objects" + str(counter_nir)
print "All labeled NIR objects" + str(counter)