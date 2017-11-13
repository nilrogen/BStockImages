"""
" Google Images API handler
"""
import requests as rq
import json

_CX = '005275668999203521604:ggwemehzrr4'
_KEY = 'AIzaSyD-u_0UdLWJcjuq4hII1WkcD8h2iK9cQW4'
_ADDR = 'https://www.googleapis.com/customsearch/v1'

TEST_QUERY = 'Costco 1146801 ADIDAS HOODIE BLACK M'
TEST_PATH = 'C:\Users\Mike Work\Desktop\out2.json'

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
    print retv.content

    jsn = json.loads(retv.content)
    retv.close()

    fout = open(TEST_PATH, 'wb')
    json.dump(jsn, fout, indent=4, separators=(',', ': '))
    fout.close()
    
