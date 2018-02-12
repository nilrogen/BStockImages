import sys, os
sys.path.append(os.getenv('HOME'))

import BStockImages.util.manifestparser as mp
import BStockImages.util.images as img

import glob

from productapi import *

from config import *
import bottlenose as bn

from lxml import etree
from lxml import objectify

AMZD = {
    'asin' : 'asin'
}

if __name__ == '__main__':
    il = ItemLookup('DE')
    for fname in glob.glob('*.csv'):
        fin = open(fname, 'r')
        mpl = mp.ManifestParser(fin, AMZD)

        for asn in mpl:
            lv = il.lookupASIN(asn['asin'])

            img.download_image(lv.getImage(), 'test/'+asn['asin']+'.jpg')
            sys.stdout.flush()


        fin.close()

