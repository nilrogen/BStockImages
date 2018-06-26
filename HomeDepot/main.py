import os, sys
sys.path.append(os.getenv('HOME'))

from BStockImages.util.db.dbmongo import getClient
from BStockImages.util.images import *
import BStockImages.util.manifestparser as mp

import glob
import argparse

from searchthd import *
from random import shuffle
from time import sleep

CSVMAP = {
    'model-num' : 'SKU',
    'description' : 'Item Name'
}

def _set(keyi, keyo, searchinfo, mapping):
    value = searchinfo[keyi]
    if value != 'None' and value != '':
        mapping[keyo] = value

def load(col):
    for fname in glob.glob('pulled/*.csv'):
        print(fname, end='')
        with open(fname, 'r') as fin:
            parser = mp.ManifestParser(fin, CSVMAP)
            for values in parser:
                values['found'] = False
                values['searched'] = False
                if col.find({'model-num' : values['model-num']}).count() == 0:
                    col.insert(values)
        print('+', flush=True)

if __name__ == '__main__':
    mongo = getClient()
    db = mongo.Items
    col = db.Homedepot

    parser = argparse.ArgumentParser()
    parser.add_argument('-l', action='store_true') 

    outfolder = 'images/%s.jpg'

    args = parser.parse_args()

    if args.l:
        load(col)
    
    itemlist = list(col.find({'searched' : False, 'found' : False}))
    shuffle(itemlist)
    
    i = 1
    ilen = len(itemlist)
    for item in itemlist:
        print('(%04d/%4d) Finding: ' % (i, ilen), item['model-num'], flush=True)
        sleep(1)
        searchinfo = searchTHD(item['model-num'])
        i += 1

        if searchinfo['model']:
            searchinfo['model'] = searchinfo['model'].split(' ')[-1]

        mapping = {}
        _set('price', 'price', searchinfo, mapping)
        _set('weight', 'weight', searchinfo, mapping)
        _set('model', 'model', searchinfo, mapping)
        _set('gtin13', 'gtin13', searchinfo, mapping)
        _set('brand', 'brand', searchinfo, mapping)
        _set('description', 'web-description', searchinfo, mapping)
        mapping['categories'] = searchinfo['categories']

        if len(mapping.keys()) == 1:
            col.update({'model-num' : item['model-num']},
                       {'$set' : {'searched' : True}})
            continue

        mapping['found'] = True
        mapping['searched'] = True

        col.update({'model-num' : item['model-num']}, {'$set' : mapping})

        try:
            img = download_image(searchinfo['url'])
            img.save(outfolder % (item['model-num']))
        except:
            pass
