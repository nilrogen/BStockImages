import os, sys
sys.path.append(os.getenv('HOME'))

from BStockImages.util.db.dbmongo import getClient

import json
from pprint import *


if __name__ == '__main__':
    mongo = getClient()
    db = mongo.Items
    col = db.Homedepot

    items = list(col.find({'searched' : True, 'found': True}))

    endlist = []

    def _set(f,t,v):
        if v in f:
            t[v]=f[v]

    for item in items:
        value = {}
        _set(item, value, 'model-num')
        _set(item, value, 'description')
        _set(item, value, 'price')
        _set(item, value, 'model')
        _set(item, value, 'gtin13')
        _set(item, value, 'web-description')
        _set(item, value, 'categories')
        
        endlist.append(value)

    with open('THD-Out.json', 'w') as fout:
        json.dump(endlist, fout,  indent='\t')
        

    
    
    

