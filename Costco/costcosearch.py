import config

import BStockImages.util.db.dbmongo as dbm
from BStockImages.util.images import *

import requests as rq
import re 
from random import shuffle

from html.parser import HTMLParser

from pprint import *

import json
import os

import PIL as pil
import PIL.Image as image

_CLOTHING_REGEX = re.compile('var products = (\[.*?\]);\r', re.DOTALL)

class CostcoParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.found = False
        self.itemnum = -1
        self.description = ""
        self.pictureurl = ""

    def handle_data(self, data):
        if self.description == '-1':
            self.description = data

    def handle_starttag(self, tag, attrs):
        if tag == 'h1' and ('itemprop', 'name') in attrs:
            self.description = '-1'
            
        if self.found:
            return 
            
        if tag == 'span' and self.itemnum == -1:
            for k,v in attrs:
                if 'data-sku' == k:
                    print('Sku')
                    self.itemnum = int(v)
                    if self.pictureurl != "":
                        self.found = True
                    break
        if tag == 'img' and self.pictureurl == "":
            if ('id', 'initialProductImage') in attrs:
                for k, v in attrs:
                    if k == 'src':
                        self.pictureurl = v
                        if self.itemnum != -1:
                            self.found = True
                        break


def _testClothing(request):
    result = _CLOTHING_REGEX.search(request.text)

    if result == None:
        return None

    jsn = json.loads(result.group(1))

    retv = []
    for item in jsn[0]:
        try:
            itemnumber  = item['partNumber']
            description = item['productName']
            url         = item['parent_img_url']

            retv.append((itemnumber, description, url))
        except KeyError as e:
            print("Error --- ", jsn)
    return retv
     
def searchCostco(itemnum):
    URL = 'https://www.costco.com/.product.html?dept=All&catalogId=0&keyword=%s'
    HEADER = { 'User-Agent' : 'Mozilla/5.0' }

    parse = CostcoParser()

    retv = None
    with rq.get(URL % itemnum, headers=HEADER) as req:
        if req.status_code == 200:
            parse.feed(req.text)
            if parse.found:
                retv = [(itemnum, parse.description, parse.pictureurl)]
            else:
                retv = _testClothing(req)
    return retv

if __name__ == '__main__':
    # Setup DB
    client = dbm.getClient()
    db = client.Items
    col = db.costco

    #searchCostco(1168584)

    items = list(col.find({
        'searched': True, 
        'found': False, 
        'reasons.website' : {
            '$exists' : False
        }
    }))
    shuffle(items)

    path = os.path.join(os.getenv('home'), 'Images')
    os.chdir(path)

    for i in range(10000):
        srcitm = items[i]
        print('Searching (%d) %d - ' % (i, srcitm['item-num']), end = '', flush=True)
        results = searchCostco(srcitm['item-num'])
        
        if results == None:
            continue
        multi = 0

        img = None
        for itn, des, url in results:
            print(itn, des, url, flush=True)
            dbitem = col.find_one({'item-num' : itn})
            if dbitem != None and dbitem['found']:
                continue

            if multi == 0:
                img = download_image(url)
                if img == None:
                    print('Image does not exist', itn)
                    break
                img.save(str(itn) + '.jpg')
                multi += 1
            else:
                img.save(str(itn) + '.jpg')  
               
            reason = {
                'success' : True,
                'website' : True,
                'description' : des,
                'imglink' : url
            }
            if dbitem != None and dbitem['found'] != True:
                query = {'$set' : { 'found': True, 
                                    'searched' : True,
                                    'image-name' : str(itn) + '.jpg',
                                    'reasons' : reason }}
                col.update({'_id' : dbitem['_id']}, query)
            else:
                ins = {
                    'item-num' : itn,
                    'searched' : True,
                    'found' : True,
                    'description' : des,
                    'image-name' : str(itn) + '.jpg',
                    'reasons' : reason
                }
                col.insert(ins)
