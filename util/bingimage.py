from PIL import Image 

import requests as rq
import json
import os
import urllib

_ADDR = 'https://api.cognitive.microsoft.com/bing/v7.0/images/search'

class bingValueResult(object):
    def __init__(self, jsn):
        self.jsn = jsn

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
        with rq.get(self.contentLink(), stream=True, headers=HEADERS) as imgreq:
            if imgreq.status_code != 200:
                raise Exception('Something is wrong. {} {}'.format(imgreq.status_code, self.contentLink()))
            imgreq.raw.decode_content = True
            img = Image.open(imgreq.raw)

        return img

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
    _headers = {'Ocp-Apim-Subscription-Key' : _KEY,
               'User-agent' : 'Mozilla/5.0' }
    fquery = { 'q' : query } 
    with rq.get(_ADDR, fquery, headers=_headers) as request:
        #print(request.json())
        return bingResults(request.json())
