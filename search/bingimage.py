"""
This module contains the classes and functions necessary to query Bing
using Microsoft azure cognitive services. Azure keys are contained in 
a keys.csv file, which should be added manually.

Functions:
    imageSearch - The function to use to grab images.
Classes:
    BingResult - Stores the results of a Bing search (a list of images and metadata)
    BingValueResult - Stores a single image and its associated metadata

@author: Michael Gorlin
@date: 2018-02-22
"""
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
    """
    This class stores the values of a single search result. It provides
    methods to navigate the result structure and return the name, host
    location, content link, and encoding for a result. It also provides
    a function to download the image. 
    """
    def __init__(self, jsn):
        self.jsn = jsn
        self.img = None

    def name(self):
        """ The name of a result is its description """
        return self.jsn['name']

    def hostLocation(self):
        """ The host location is the base url of the host """
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

def imageSearch(query, cc='en-US'):
    _headers = {'Ocp-Apim-Subscription-Key' : _KEY1,
                'User-Agent' : 'Mozilla/5.0' }
    global _SESSION

    if not _SESSION:
        _SESSION = rq.Session()
    fquery = { 'q' : query , 'mkt' : cc} 
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
