import requests as rq
import json
import os
import urllib

#_KEY = 'd18843648d3147dc9f6dc021e4a85a97'
_KEY = '796faf0051e14fba9809d5fbe013c7a5'
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

class bingResults(object):
    def __init__(self, jsn):
        self.jsn = jsn

    def matchCount(self):
        return self.jsn['totalEstimatedMatches']

    def values(self):
        if self.matchCount() != 0:
            return self.jsn['value']
        return 0
    
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

_SAVE_PATH = os.path.join(os.getenv('HOME'), 'Images')
if __name__ == '__main__':
    st = 'costco 922243 KS 159PC MECHANICS TOOL'

    print('Querying Bing')
    with imageSearch(st) as results:
        print(results.ok)
        print(results)
        if results.ok:
            print('Results returned')
            with open(os.path.join(_SAVE_PATH, 'azureout.json'), 'w') as fout:
                print('Saving JSON')
                json.dump(results.json(), fout, indent=4)
            

