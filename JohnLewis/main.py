import os, sys
sys.path.append(os.getenv('HOME'))

from BStockImages.util.db.dbmongo import getClient
from BStockImages.util.images import *

import BStockImages.util.manifestparser as mp

from searchjl import *

import glob
import argparse
from random import shuffle
from time import sleep

CSVMAP = {
    'product-code' : 'Product Code',
    'description'  : 'Description'
}

def load(col):
    i = 1
    files = glob.glob('manifests/*.csv')
    lfiles = len(files)
    for fname in files:
        print('(%3d/%3d)'%(i, lfiles), fname, end='', flush=True)
        fin = open(fname, 'r', encoding='utf-8', errors='ignore')
        parser = mp.ManifestParser(fin, CSVMAP)
        for rows in parser:
            rows['searched'] = False
            rows['found'] = False
            if col.find({'product-code' : rows['product-code']}).count() == 0:
                col.insert(rows)
        fin.close()
        i += 1
        print('+', flush=True)
                

if __name__ == '__main__':

    mongo = getClient()
    db = mongo.Items
    col = db.JohnLewis

    parser = argparse.ArgumentParser()
    parser.add_argument('-l', action='store_true') 
    
    args = parser.parse_args()
    if args.l:
        load(col)

    itemlist = list(col.find({'searched':False, 'found':False}))
    shuffle(itemlist)

    i = 1
    litemlist = len(itemlist)
    for item in itemlist:
        print('(%04d/%4d) Finding %s' %(i, litemlist, item['product-code']), flush=True)
        i+=1 

        svalue = searchJohnLewis(item['product-code'])

        if svalue['url'] == None:
            col.update({'product-code' : item['product-code']}, \
                       {'$set' : {'searched' : True}})

            continue

        try:
            print(svalue['url'])
            img = download_image(svalue['url'])
            img.save('images/%s.jpg' % (item['product-code']))
        except:
            continue

        col.update({'product-code' : item['product-code']}, \
                   {'$set' : { 'searched' : True, 'found' : True }})
        print('+', flush=True)
        sleep(5)


