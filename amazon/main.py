import config
import sys

import BStockImages.util.manifestparser as mp

from BStockImages.util.db.dbmongo import getClient
from BStockImages.util.images import download_image

import glob
import time
from random import shuffle

from productapi import *

AMZD = {
    'asin' : 'Asin',
    'region' : 'InventoryLocation',
    'description' : 'ItemDesc'
}

def getEXT(ext):
    if ext == 'JPEG':
        return 'jpg'
    elif ext == 'GIF':
        return 'gif'
    

if __name__ == '__main__':
    mongo = getClient()
    db = mongo.Items
    col = db.Amazon

    MKT = 'DE'

    il = ItemLookup(MKT)

    fquery = { 
        'region' : MKT, 
        'found' : False,
        'searched' : True
    }

    itemlist = list(col.find(fquery))
    shuffle(itemlist)

    if len(itemlist) == 0:
        exit()

    for item in itemlist:
        print('FINDING: ', item['asin'], item['description'], flush=True)
        # Lookup
        lookupvalue = il.lookupASIN(item['asin'])
        if not lookupvalue:
            # Not found
            col.update({'asin' : item['asin']}, {'$set' : {'searched':True}})
            continue

        # Get Image URL
        lvimg = lookupvalue.getImage()
        if not lvimg:
            col.update({'asin' : item['asin']}, {'$set' : {'searched':True}})
            continue

        # Download Image
        dimg = download_image(lvimg)
        if not dimg != None:
            continue

        # Save Image
        dimg.save('test/'+item['asin'] + '.' +  getEXT(dimg.format))
        dimg.close()

        # Update DB
        reason = {
            'searched' : True,
            'found' : True,
            'reasons' : {
                'website' : True,
                'link' : lvimg
            }
        }
        col.update({'asin' : item['asin']}, {'$set' : reason})

