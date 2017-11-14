"""
" Google Images API handler
"""
import requests as rq
import json

_CX = '005275668999203521604:ggwemehzrr4'
_KEY = 'AIzaSyD-u_0UdLWJcjuq4hII1WkcD8h2iK9cQW4'
_ADDR = 'https://www.googleapis.com/customsearch/v1'

class searchResult(object):
    """
    " Helpful items
    " jsn['items']                   - List of search results
    " jsn['items'][i]                - An item in the results
    " jsn['items'][i]['displayLink'] - The base website of image (www.costco.com)
    " jsn['items'][i]['link']        - The link for the image
    " jsn['items'][i]['mime']        - The type of image (image/jpeg)
    "
    " jsn['searchInformation']['totalResults'] - Number of results
    """
    def __init__(self, _jsn):
        self.jsn = _jsn

    def totalResults(self):
        return self.jsn['searchInformation']['totalResults']

    def itemList(self):
        return self.jsn['items']

def imageSearch(query):
    params = { 'cx' :  _CX,
               'key' : _KEY,
               'searchType' : 'image',
               'q' : query }
    
    return rq.get(_ADDR, params)

def toJSON(req):
    return json.loads(req.content)


if __name__ == '__main__':
    retv = imageSearch(TEST_QUERY)
    print(retv.content)

    jsn = json.loads(retv.content)
    retv.close()

    fout = open(TEST_PATH, 'wb')
    json.dump(jsn, fout, indent=4, separators=(',', ': '))
    fout.close()
    
