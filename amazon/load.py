import config
import sys
import BStockImages.util.manifestparser as mp

from BStockImages.util.db.dbmongo import getClient
from BStockImages.util.images import download_image

import glob
import math

AMZD = {
    'asin' : 'Asin',
    'region' : 'InventoryLocation',
    'description' : 'ItemDesc',
    'cost' : ('TotalCost', 0)
}

if __name__ == '__main__':
    mongo = getClient()
    db = mongo.Items
    col = db.Amazon


    # Parse CR manifests
    for fname in glob.glob('manifests/*_CR_*.csv'):
        print(fname, flush=True)
        fin = open(fname, 'r', encoding='utf-8')
        mpl = mp.ManifestParser(fin, AMZD)

        lst = []
        for k in mpl:
            lst.append(k)

        lst = sorted(lst, key=lambda v: float(v['cost']), reverse=True)
        lst = lst[:math.floor(.5 * len(lst))]

        for asn in lst:
            asn['searched'] = False
            asn['found'] = False
            asn.pop('cost', None)
            if col.find({'asin' : asn['asin']}).count() == 0:
                col.insert(asn)

        fin.close()
        print('Done')
