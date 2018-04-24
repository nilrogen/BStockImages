import os,sys
sys.path.append(os.getenv("HOME"))

from BStockImages.util.sitesearching import *
from BStockImages.util.images import *
import BStockImages.util.manifestparser as mp

from searchappliances import *


if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit()

    sbrand = sys.argv[1]
    fout = 'samples/%s/%s.jpg'

    try:
        os.mkdir('samples/%s' % sbrand)
    except:
        pass

    itemset = []

    with open('%s.csv' % sbrand, 'r') as fin:
        manifest = mp.ManifestParser(fin, {'model' : 'MODEL',  \
                                           'brand' : 'BRAND'})

        for v in manifest:
            itemset.append((v['model'], v['brand'].split(' ')[0]))
        
        print(len(set(itemset)))

        for model, brand in set(itemset):
            print('Searching', brand, model, flush=True)
            items = search_appliance_connection(model, brand)
            if not items:
                print(model, 'Not Found\n')
                continue

            pprint(items)
            print(flush=True)

            img = download_image(items['url'])
            img.save(fout % (sbrand, items['model'].lower()))


    
