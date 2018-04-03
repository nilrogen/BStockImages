import sys, os
sys.path.append(os.getenv('home'))

import BStockImages.util.manifestparser as mp
from BStockImages.util.db.dbmongo import getClient
from BStockImages.util.images import download_image
from BStockImages.util.imagepulling import *

from html.parser import HTMLParser

import requests as rq

from pprint import *

THDPM = {
    'price'       : Tag('span', 'id', 'ajaxPrice', 'content'),
    'weight'      : Content('div', 'itemprop', 'weight'),
    'description' : Content('h1', 'class', 'product-title__title'),
    'brand'       : Content('h2', 'class', 'product-title__brand'),
    'model'       : Content('h2', 'class', 'product_details modelNo'),
    'gtin13'      : InsideContent('div', 'upc', 'class', 'product-title'),
    'url'         : Tag('img', 'id', 'mainImage', 'src')
}

def searchTHD(modelnum):
    URL = 'http://www.homedepot.com/s/%s' % modelnum
    parser = MarketplaceParser(THDPM)

    search_site(URL, parser)

    return parser.getValues()

if __name__ == '__main__':

    pprint(searchTHD('1000051192'))
