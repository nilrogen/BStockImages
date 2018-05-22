import sys, os
sys.path.append(os.getenv('home'))

import BStockImages.util.manifestparser as mp
from BStockImages.util.images import download_image
from BStockImages.util.sitesearching import *

import requests as rq


import webbrowser
JLHTMLP = {
    'url' : InsideAttribute('div', 'img', 'id', 'carousel-wrapper', 'src')
}

def searchJohnLewis(productcode):
    URL = 'https://www.johnlewis.com/search/%s' % productcode
    parser = MarketplaceParser(JLHTMLP)

    search_site(URL, parser)

    retv = parser.getValues()
    if retv['url']:
        retv['url'] = "http:" + retv['url']

    return retv


    

