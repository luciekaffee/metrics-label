wget https://dumps.wikimedia.org/wikidatawiki/entities/latest-truthy.nt.bz2
bzip2 -d latest-truthy.nt.bz2

echo "total entities"
wc -l latest-truthy.nt
cat latest-truthy.nt | grep -E "schema.org/name|skos/core#altLabel|schema.org/description" | awk '{print $1}' | sort | uniq > labeled-entities.csv
#awk '{print $1}' wikidata-labels.csv | sort | uniq > labeled-entities.csv
echo "entities with labels"
wc -l labeled-entities.csv
cat latest-truthy.nt | awk '{print $3}' | grep www.wikidata.org/entity/Q | sort | uniq > objects.csv
echo "Total unique objects"
wc -l objects.csv
echo "Total unique objects with label"
grep -Fwf objects.csv labeled-entities.csv | wc -l
