import sys, os
sys.path.append(os.getenv('home'))

import BStockImages.util.manifestparser as mp
from BStockImages.util.db.dbmongo import getClient
from BStockImages.util.images import download_image
from BStockImages.util.sitesearching import *

import requests as rq

from pprint import *

import re
import json

THDHTMLPM = {
    'price'       : Tag('span', 'id', 'ajaxPrice', 'content'),
    'weight'      : Content('div', 'itemprop', 'weight'),
    'description' : Content('h1', 'class', 'product-title__title'),
    'brand'       : Content('h2', 'class', 'product-title__brand'),
    'model'       : Content('h2', 'class', 'product_details modelNo'),
    'gtin13'      : InsideContent('div', 'upc', 'class', 'product-title'),
    'url'         : Tag('img', 'id', 'mainImage', 'src')
}

MP = {
    'upc' : 'UPC'
}

_CAT_REGEX = re.compile('var BREADCRUMB_JSON = ({.*?});', re.DOTALL)

def findCategories(html, values):
    dept   = None
    cat    = None
    subcat = None

    # Search
    result = _CAT_REGEX.search(html)
    
    if result:
        retv = json.loads(result.group(1))
        return retv['bcEnsightenData']['contentSubCategory'].split('>')

    return []

def searchTHD(modelnum):
    URL = 'http://www.homedepot.com/s/%s' % modelnum
    #webbrowser.open_new_tab(URL)h
    parser = MarketplaceParser(THDHTMLPM)
    html = search_site(URL, parser)
    
    values = parser.getValues()
    values['categories'] = findCategories(html, values)
    for k in THDHTMLPM:
        THDHTMLPM[k].reset()

    return values
