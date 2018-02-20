import sys
import os
sys.path.append(os.getenv('HOME'))

import MySQLdb as sql

import BStockImages.util.manifestparser as mp

from BStockImages.util.db.dbobjects import * 
from BStockImages.util.db.dbmanager import *
from BStockImages.util.db.config import *

_FILE = 'sample.csv'

wpdict = {
    ModelNumber       : 'Model',
    Description       : 'Model Desc',
    mktCategory       : 'Product Type',
    mktSubcategory    : 'Product Sub-Type',
    RetailPrice       : 'Price',
    MSRP              : 'MSRP'
}

ldict = {
    ModelNumber       : 'Model Number',
    Brand             : 'Manufacturer Brand Name',
    mktCategory       : 'Product Category',
    mktSubcategory    : 'Product Sub-Category',
    SKU               : "Lowe's Item Number",
    Description       : "Lowe's Item Description",
    MAP               : 'MAP Value'
}

adict = {
    ModelNumber : 'Part Number',
    Brand       : 'Manufacturer', 
    mktCategory : 'Auction Category',
    Description : 'Title',
    ShipWeight  : 'Weight',
    MSRP        : MSRP,
    'num'       : 'Qty'
}

bbdict = {
    mktCategory    : 'CATEGORY',
    mktSubcategory : 'SUB-CATEGORY',
    Brand          : 'BRAND',
    ModelNumber    : 'MODEL',
    SKU            : 'SKU',
    Description    : 'SKU DESCRIPTION',
    Weight         : 'UNIT WEIGHT',
    RetailPrice    : 'RETAIL'
}


if __name__ == '__main__':
    conn = sql.Connect(user='root', passwd='password', db='BStock')

    def read_all(dbm, dirname, mapping, fn=lambda a: a):
        # Read files in directory
        for fname in os.listdir(dirname):
            # open file
            with open(os.path.join(dirname, fname), 'r') as fin:
                # Parse and read each line
                manp = mp.ManifestParser(fin, mapping)
                for manifestrow in manp:
                    try:
                        fn(manifestrow)
                        if manifestrow[ModelNumber] == None:
                            continue

                        # Load values
                        it = Item.load_values(manifestrow)
                        ide = ItemDescription.load_values(manifestrow)

                        # add information
                        dbm.addInformation(it, ide)
                    except Exception as e:
                        print(e, type(e), fin)
        

    def handle(d):
        d[MSRP] = float(d[MSRP])/float(d['num'])
        d[ShipWeight] = float(d[ShipWeight])/float(d['num'])

    dbm = DBManager(conn, 'Almo')
    read_all(dbm, 'asamples', adict, handle)

    dbm = DBManager(conn, 'Whirlpool') 
    read_all(dbm, 'wsamples', wpdict)

    dbm = DBManager(conn, 'Lowes')
    read_all(dbm, 'lsamples', ldict)

    dbm = DBManager(conn, 'BestBuy')
    read_all(dbm, 'bbsamples', bbdict)


    conn.close()

