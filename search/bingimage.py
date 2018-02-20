from PIL import Image 

import requests as rq
import json
import os
import urllib

_KEY1 = None
_KEY2 = None
def getKeys():
    import csv
    global _KEY1, _KEY2
    filedir = os.path.dirname(os.path.abspath(__file__))

    if _KEY1 == None or _KEY2 == None:
        with open(os.path.join(filedir,'keys.csv')) as fin:
            reader = csv.reader(fin)
            _KEY1 = str(next(reader)[1])
            _KEY2 = str(next(reader)[1])
getKeys()

_ADDR = 'https://api.cognitive.microsoft.com/bing/v7.0/images/search'
_SESSION = None

class bingValueResult(object):
    def __init__(self, jsn):
        self.jsn = jsn
        self.img = None

    def name(self):
        return self.jsn['name']

    def hostLocation(self):
        return urllib.parse.urlsplit(self.jsn['hostPageUrl']).netloc

    def contentLink(self):
        return self.jsn['contentUrl']

    def contentEncoding(self):
        return self.jsn['encodingFormat']

    def downloadImage(self):
        HEADERS = {'User-agent': 'Mozilla/5.0'}

        if self.img is not None:
            return self.img
            
        with rq.get(self.contentLink(), stream=True, headers=HEADERS) as imgreq:
            if imgreq.status_code != 200:
                raise Exception('Something is wrong. {} {}'.format(imgreq.status_code, self.contentLink()))
            imgreq.raw.decode_content = True
            self.img = Image.open(imgreq.raw)

        return self.img

class bingResults(object):
    def __init__(self, jsn):
        self.jsn = jsn

    def matchCount(self):
        if 'totalEstimatedMatches' in self.jsn.keys():
            return self.jsn['totalEstimatedMatches']
        return 0

    def values(self):
        if self.matchCount() != 0:
            return self.jsn['value']
        return []
    def valueCount(self):
        return len(self.values())
   
    def getValue(self, i):
        return bingValueResult(self.values()[i])

def imageSearch(query):
    _headers = {'Ocp-Apim-Subscription-Key' : _KEY1,
                'User-agent' : 'Mozilla/5.0' }
    global _SESSION

    if not _SESSION:
        _SESSION = rq.Session()
    fquery = { 'q' : query } 
    retv = None
    try:
        with _SESSION.get(_ADDR, params=fquery, headers=_headers) as request:
            if request.status_code == 200:
            #print(request.json())
                retv = bingResults(request.json())
                return retv
            return None
    except Exception as e:
        print(e, type(e), 'There was an issue with processing the json result!', flush=True)
        raise
