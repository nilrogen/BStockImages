import os, sys
sys.path.append(os.getenv('HOME'))

import BStockImages.util.manifestparser as mp

from requests import post
import webbrowser

from pprint import *

DIN = { 'st' : 'Description Part Number' }

st = 'pww networkms'
url = 'https://www.cdw.com/'

_HEADERS = {
    'User-Agent' : 'Mozilla/5.0' 
}

if __name__ == '__main__':
    with open('m1.csv', 'r') as fin:
        parser = mp.ManifestParser(fin, DIN)

    with post(url, data={'Search' : st}, headers=_HEADERS) as req:
        pprint(req.headers)
        print(req.status_code)
        

