"""
" procman.py
"
" This file processes the manifests. Either by being run as a script where it
" will add to the previous AllItems.json; or as a module where it has 
" functions to read the contents of that file. 
"""
from items import *
from config import _FNAME, _MANIFEST_PATH, _IMAGES_PATH

from countfiles import *

import json
import os

itemjson = None
itemlist = None

def setall():
    global itemjson, itemlist
    if itemjson == None:
        with open(_FNAME, 'r') as allitems:
            itemjson = json.load(allitems)
    if itemlist == None:
        itemlist = list(map(Item.fromJSON, itemjson['items']))
    
def getItemJson():
    setall()
    return itemjson

def getItemList():
    setall()
    return itemlist

def applyFilter(fn):    
    setall()
    return list(filter(fn, itemlist))

def getFound():
    return applyFilter(lambda item: item.found)

def getMissing():
    return applyFilter(lambda item: not item.found)

    
"""
def update():
    global itemlist, itemjson
    missing = getMissing()
    imgs = list(map(lambda x: os.path.splitext(x)[0]), \
                    os.listdir(_IMAGES_PATH))

    for item in missing:
        if str(item.itemnum) in imgs:
"""
        
        


if __name__ == '__main__':
    try:
        # Otherwise print all manifests that have items that have been found
        with open(_FNAME, 'r') as allitems:
            pass
    except FileNotFoundError:
        jsn = { 'processed' : False, 'count' : 0, 'found' : 0 }
        
        # Loop through each manifest and add each item to jsn['items']
        os.chdir(_MANIFEST_PATH)
        itemlist = set()
        for manifest in os.listdir():
            with open(manifest) as fin:
                parseCSV(itemlist, fin)

        imagelist = sorted(itemlist)
        for image in os.listdir(_IMAGES_PATH):
            basename, ext = os.path.splitext(image)
            for item in itemlist:
                if int(basename) == item.itemnum:
                    item.found = True
                    item.imagename = '{}{}'.format(basename, ext)
                    jsn['found'] += 1
                    break
        allitems = open(config._FNAME, 'w')

        jsn['count'] = len(itemlist)
        jsn['processed'] = True
        jsn['items'] =  list(map(lambda itm: Item.toJSON(itm), itemlist))

        json.dump(jsn, allitems, indent=4)
