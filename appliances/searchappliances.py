import os,sys
sys.path.append(os.getenv("HOME"))

from BStockImages.util.sitesearching import *
from BStockImages.util.images import *
from pprint import *

import webbrowser

APPLIANCE_CONNECTION_PARSE_INFO = {
   'url'   : Tag('img', 'id', 'productImage', 'src'),
   'model' : InsideContent('h1', 'b', 'class', 'product-model')
}

_AC_URL = 'https://www.appliancesconnection.com/%s-%s.html'
def search_appliance_connection(modelnumber, brand):
    parser = MarketplaceParser(APPLIANCE_CONNECTION_PARSE_INFO)

    url = _AC_URL % (brand.lower(), modelnumber.lower())


    search_site(url, parser)

    retv = parser.getValues()
    if modelnumber.lower() != retv['model'].lower():
        return None

    return retv


if __name__ == '__main__':
    import BStockImages.util.manifestparser as mp
    
    brand = 'lg'

    fout = 'samples/%s.jpg'
    
    itemset = []

    with open('brands.csv', 'r') as fin:
        manifest = mp.ManifestParser(fin, {'model' : 'MODEL'})

        for v in manifest:
            itemset.append(v['model'])
        
    print(len(set(itemset)))
"""
            items = search_appliance_connection(v['model'], brand)
            pprint(items)
            print(flush=True)

            img = download_image(items['url'])
            img.save(fout % items['model'].lower())
            """
