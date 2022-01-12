from elasticsearch import Elasticsearch
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

es = Elasticsearch()
res = es.search(index="iris", doc_type="flowers", size=1000)

df = pd.json_normalize(res['hits']['hits'])
df.rename( 
    columns={
        '_source.Id': 'Id', 
        '_source.SepalLengthCm': 'SepalLengthCm', 
        '_source.PetalLengthCm':'PetalLengthCm', 
        '_source.PetalWidthCm':'PetalWidthCm', 
        '_source.Species': 'Species'}, inplace=True)


test = sns.load_dataset('iris')
g = sns.pairplot(test,hue="species")

plt.show()