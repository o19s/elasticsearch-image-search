
from elasticsearch import Elasticsearch
from PIL import Image
import os

es = Elasticsearch()

def images():
    for f in os.listdir('img'):
        fName, fExt = os.path.splitext(f)
        if fExt == '.jpg':
            imgId = fName
            imgF = Image.open(os.path.join('img', f))
            yield (imgId, imgF)


def tokens(img):
    resized = img.resize((50, 50))
    for idx, (r, g, b) in enumerate(resized.getdata()):
        yield "%s_%s_%s_%s" % (idx, int(r/10), int(g/10), int(b/10))

def indexImg(imgId, tokens):
    es.index('images', doc_type='image', id=imgId, body={'bmp': tokens})



for imgId, img in images():
    print("Indexing %s" % imgId)
    indexImg(imgId, [token for token in tokens(img)])
