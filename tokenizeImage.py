
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


def tokens(imgF):
    for idx, (r, g, b) in enumerate(imgF.getdata()):
        yield "%s_%s_%s_%s" % (idx,  r/10, g/10, b/10)

def indexImg(imgId, tokens):
    es.index('images', doc_type='image', id=imgId, body={'bmp': tokens})



for imgId, img in images():
    indexImg(imgId, [token for token in tokens(img)])
