import os, sys
sys.path.append(os.getenv('HOME'))

import BStockImages.util.manifestparser as mp

from BStockImages.util.sitesearching import *
from BStockImages.util.images import download_image

from argparse import *
import webbrowser

import re

LAYER1_OPT = {
    'url' : Tag('button', 'class', 'pure-button wg fill-to-top', 'href')
}

LAYER2_OPT = {
    'url' : Tag('div', 'class', 'product-image-wrapper', 'style') 
}

CSVMAP = {
    'item-num' : 'Item Number'
}

REGEX = re.compile("url\('(.*)'\)")

def search_layer1(itemnum):
    URL = 'https://www.pirch.com/search?query=%s' % itemnum
    parser = MarketplaceParser(LAYER1_OPT)

    search_site(URL, parser)

    retv = parser.getValues()
    if retv['url']:
        search_layer2(itemnum, retv['url'])

def search_layer2(itemnum, url):
    URL = 'https://www.pirch.com%s' % url

    parser = MarketplaceParser(LAYER2_OPT)
    search_site(URL, parser)

    retv = parser.getValues()
    if retv['url']:
        imgurl = REGEX.search(retv['url']).group(1)
        try:
            img = download_image(imgurl)
            img.save('images/%s.jpg' % itemnum)
        except Exception as e:
            print(e)


def find_images(fname):
    fin = open(fname, 'r', encoding='utf-8', errors='ignore')
    parser = mp.ManifestParser(fin, CSVMAP)

    for row in parser:
        itemnum = row['item-num']
        print(itemnum, flush=True)
        search_layer1(itemnum)

    fin.close()
    

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('files', nargs='+')

    args = parser.parse_args()

    for fname in args.files:
        find_images(fname)

