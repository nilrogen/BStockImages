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



if __name__ == '__main__':
    try:
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
