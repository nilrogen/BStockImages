"""
" This script takes Amazon manifests and loads them into a MongoDB database.
" The location of the manifests are passed in as arguments to the script.
"
" Author: Michael Gorlin
"""
import config
import os
import sys
import BStockImages.util.manifestparser as mp

from BStockImages.util.db.dbmongo import getClient
from BStockImages.util.images import download_image

import argparse
import glob
import math

""" 
" This dictionary is used for parsing each manifest, the keys represent the 
" output keys, and their values are the manifest column names.
"""
AMZD = {
    'asin' : 'Asin',
    'region' : 'InventoryLocation',
    'description' : 'ItemDesc',
    'cost' : ('TotalCost', 0)
}

if __name__ == '__main__':
    # Load mongodb
    mongo = getClient()
    db = mongo.Items
    col = db.Amazon

    parser = argparse.ArgumentParser('Amazon manifest loader')
    parser.add_argument('dirs', nargs='+', help='Manifest Directories')
    
    args = parser.parse_args()

    for directory in args.dirs:
        if not os.path.isdir(directory):
            print(directory, 'does not exist.')
            continue

        # Parse CR manifests
        for fname in glob.glob('%s/*_CR_*.csv' % directory):
            print(fname, flush=True)

            fin = open(fname, 'r', encoding='utf-8')

            # Manifest parser takes a csv and converts rows into json.
            mpl = mp.ManifestParser(fin, AMZD)

            lst = []
            for items in mpl:
                lst.append(items)

            # Sort manifest contents by cost and eliminate bottom 50%
            lst = sorted(lst, key=lambda v: float(v['cost']), reverse=True)
            lst = lst[:math.floor(.5 * len(lst))]

            for asn in lst:
                # Add metadata for database items and remove cost
                asn['searched'] = False
                asn['found'] = False
                asn.pop('cost', None)
                # insert if not present in the database
                if col.find({'asin' : asn['asin']}).count() == 0:
                    col.insert(asn)

            fin.close()
            print('Done')
