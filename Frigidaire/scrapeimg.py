from config import _IMAGES_TMP
from model import *

import requests
import webbrowser
import locale
import os
import sys
import json

import readmodels as rm

from random import randint, shuffle
from html.parser import HTMLParser

import PIL as pil
import PIL.Image as Image

class FrigidaireParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.imagelink = None
        self.script = False
        self.data = ''

        # State for finding product weight
        self.li = 0 
        self.productweight = ''
        self.shippingweight = ''
        
    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            if ('id', 'product_image') in attrs:
                for k, v in attrs:
                    if k == 'src':
                        self.imagelink = v
        if tag == 'script' and self.data == '':
            self.script = True

        if tag == 'li':
            self.li += 1
        

    def handle_data(self, data):
        if self.script and data.find('var mpGlobalProperties') != -1:
            self.data = data[data.find('{'):data.find('}')+1]
            self.script = False

        if self.li != 0:
            if data.find('Product Weight') != -1:
                self.productweight = data
            elif data.find('Shipping Weight') != -1:
                self.shippingweight = data

    def handle_endtag(self, tag):
        if self.li != 0:
            if tag == 'li':
                self.li -= 1

def msrp_parse(value):
    locale.setlocale(locale.LC_ALL, '')
    curchar = locale.localeconv()['currency_symbol']
    return locale.atof(value.strip(curchar))

def handle_request(req, item):
    if req.status_code == 200:
        sys.stdout.flush()

        #webbrowser.open(linkstr.format(item.modelnumber))               
        parser = FrigidaireParser()
        parser.feed(req.text)

        data = json.loads(parser.data)

        item.setfromWebData(data)

        item.weight = parser.productweight
        item.shipweight = parser.shippingweight

        if parser.imagelink != '':
            imagesrc = 'https:{}'.format(parser.imagelink)
            if imagesrc.find('error') == -1 and imagesrc.find('mp4') == -1:
                item.imagesrc = imagesrc
                item.found = True
    item.searched = True

if __name__ == '__main__':
    lst = rm.generateList()

    totalitems, founditems = len(lst), 0

    shuffle(lst)

    linkstr = 'https://www.frigidaire.com/Kitchen-Appliances/Refrigerators/French-Door-Refrigerator/{}/'

    pstring = '{:<10} - {:>4}/{:<4} ({:.3}%)'

    for index in range(len(lst)):
        item = lst[index]

        print(pstring.format(item.modelnumber, 
                             index,
                             totalitems, 
                             100.0 * index / float(totalitems)),
              end='')
        sys.stdout.flush()

        with requests.get(linkstr.format(item.modelnumber)) as req:
            try:
                handle_request(req, item)
                if item.found:
                    print(' Found', end='')
                    founditems += 1
            except Exception as e:
                print(item.modelnumber)
                item.searched = True
        print()

    # Format AllModels.json
    itemjson = list(map(Model.toJSON, lst))
    with open('AllModels.json', 'w') as fout:
        resjsn = {
            'total-items' : totalitems,
            'found-items' : founditems,
            'model-list'  : itemjson
        }
        json.dump(resjsn, fout, indent=4)
