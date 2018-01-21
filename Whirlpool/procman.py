import sys
import os
sys.path.append(os.getenv('HOME'))

import MySQLdb as sql

import BStockImages.util.manifestparser as mp

from BStockImages.util.dbobjects import * 
from BStockImages.util.dbmanager import *
from BStockImages.util.config import *

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


if __name__ == '__main__':
    conn = sql.Connect(user='root', passwd='password', db='BStock')

    def read_all(dbm, dirname, mapping, fn=lambda a: a):
        for fname in os.listdir(dirname):
            with open(os.path.join(dirname, fname), 'r') as fin:
                manp = mp.ManifestParser(fin, mapping)
                for manifestrow in manp:
                    try:
                        fn(manifestrow)
                        if manifestrow[ModelNumber] == None:
                            continue

                        it = Item.load_values(manifestrow)
                        ide = ItemDescription.load_values(manifestrow)
                        dbm.addInformation(it, ide)
                    except Exception as e:
                        print(e, type(e), fin)
        

    def handle(d):
        d[MSRP] = float(d[MSRP])/float(d['num'])
        d[ShipWeight] = float(d[ShipWeight])/float(d['num'])

    dbm = DBManager(conn, 'Lowes')
    read_all(dbm, 'asamples', adict, handle)

    dbm = DBManager(conn, 'Whirlpool') 
    read_all(dbm, 'wsamples', wpdict)

    dbm = DBManager(conn, 'Lowes')
    read_all(dbm, 'lsamples', ldict)


    conn.close()

