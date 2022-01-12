from elasticsearch import helpers, Elasticsearch
import csv
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from flask import Flask, jsonify


app = Flask(__name__)

@app.route('/status', methods=["GET"])
def health_check():
    return jsonify(status='ok'), 200

@app.route('/loader', methods=["GET"])
def loader():
    es = Elasticsearch([os.getenv('ES_HOST')])
    with open('Iris.csv') as f:
        reader = csv.DictReader(f)
        helpers.bulk(es, reader, index='iris', doc_type='flowers')
    return jsonify(status='ok'), 200

@app.route('/viewer', methods=["GET"])
def viewer():
    es = Elasticsearch([os.getenv('ES_HOST')])
    res = es.search(index="iris", doc_type="flowers", size=1000)

    df = pd.json_normalize(res['hits']['hits'])
    df.rename( 
        columns={
            '_source.Id': 'Id', 
            '_source.SepalLengthCm': 'SepalLengthCm', 
            '_source.PetalLengthCm':'PetalLengthCm', 
            '_source.PetalWidthCm':'PetalWidthCm', 
            '_source.Species': 'Species'}, inplace=True)


    g = sns.pairplot(df,hue="Species")
    plt.show()
    return jsonify(status='ok'), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8010, debug=True)