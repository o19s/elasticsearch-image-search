from elasticsearch import Elasticsearch
from PIL import Image
from tokenizeImage import tokens

es = Elasticsearch()

from sys import argv
searchImg = argv[1]

img = Image.open(searchImg)
search = " ".join([token for token in tokens(img)])

query = {
    "query": {
        "match": {
            "bmp": {
                "query": search,
                "minimum_should_match": 1
            }
        }
    }
}

res = es.search(index="images", doc_type='image', body=query)

print(res['hits']['hits'][0]['_id'])

def indexImg(imgId, tokens):
    es.index('images', doc_type='image', id=imgId, body={'bmp': tokens})
