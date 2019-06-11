import json
import random

class DomainCreator():

    def __init__(self):
        self.query_ids = []
        with open('data/query-ids.json') as infile:
            self.query_ids = json.loads(infile)

    def get_queries_all(self, numberQueries):
        qids = self.query_ids.copy()
        random.shuffle(qids)
        chunksize = len(qids) // numberQueries



    def run(self, numberQueries, domains=None):
        if not domains:
            self.get_queries_all(numberQueries)


