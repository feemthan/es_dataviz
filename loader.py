from elasticsearch import helpers, Elasticsearch
import csv

es = Elasticsearch()

with open('Iris.csv') as f:
    reader = csv.DictReader(f)
    helpers.bulk(es, reader, index='iris', doc_type='flowers')