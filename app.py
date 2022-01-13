from elasticsearch import helpers, Elasticsearch
import csv
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns
from flask import Flask, jsonify, render_template
import pdb
plt.ioff()

app = Flask(__name__)

@app.route('/status', methods=["GET"])
def health_check():
    return jsonify(status='ok'), 200

@app.route('/loader', methods=["GET"])
def loader():

    es = Elasticsearch()#[os.getenv('ES_HOST')], port= 9200)
    with open('Iris.csv') as f:
        reader = csv.DictReader(f)
        helpers.bulk(es, reader, index='iris', doc_type='flowers')
    return jsonify(status='DATASET LOADED'), 200

@app.route('/viewer', methods=["GET"])
def viewer():
    # print(os.getenv('ES_HOST'))
    es = Elasticsearch()#[os.getenv('ES_HOST')], port= 9200)
    res = es.search(index="iris", doc_type="flowers", size=1000)

    df = pd.json_normalize(res['hits']['hits'])
    df.rename( 
        columns={
            '_source.Id': 'Id', 
            '_source.SepalLengthCm': 'SepalLengthCm', 
            '_source.PetalLengthCm':'PetalLengthCm', 
            '_source.PetalWidthCm':'PetalWidthCm', 
            '_source.Species': 'Species'}, inplace=True)

    df = df[['Id', 'SepalLengthCm', 'PetalLengthCm', 'PetalWidthCm', 'Species']]

    sns.FacetGrid(df, hue ="Species", height = 6).map(plt.scatter, 'SepalLengthCm', 'PetalLengthCm').add_legend()
    img_path = os.path.join('static', 'image.png')
    plt.savefig(img_path)
    plt.close()

    return render_template('image.html', image = img_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8040, debug=True)