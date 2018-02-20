import os
import sys
sys.path.append(os.getenv('HOME'))

import BStockImages.util.manifestparser as parse

import config
import webbrowser

if __name__ == '__main__':
    d = { 'in' : 'Costco Item #' }
    query = 'http://www.costco.com/.product.html?dept=All&keyword=%s'
    for man in os.listdir('samples'):
        with open(os.path.join('samples', man)) as fin:
            mp = parse.ManifestParser(fin, d)
            for k in mp:
                print(query % k['in'])
                webbrowser.open(query % k['in'])
        
        
        
    


