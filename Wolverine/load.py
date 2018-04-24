import sys, os
sys.path.append(os.getenv('HOME'))

import BStockImages.util.manifestparser as mp
from BStockImages.search.searchmodel import *
from BStockImages.search import *

WHITELIST = {
    'www.chaco.com'         : 1, 
    'www.sperry.com'        : 1,
    'www.wolverine.com'     : 1,
    'www.hushpuppies.com'   : 1,
    'www.saucony.com'       : 1,
    'www.nordstromrack.com' : .8
}


def getExt(s):
    if s == None:
        raise ValueError
    elif s == 'JPEG':
        return '.jpg'
    elif s == 'PNG':
        return '.png'
    else:
        return '.jpg'

class WolverineModel(SearchModel):
    def __init__(self, whitelist):
        super(WolverineModel, self).__init__('Wolverine')
        self.whitelist = whitelist

    def queryOptions(self):
        return ['BI']
    
    def saveSuccess(self, item):
        try:
            img = item.searchresult.downloadImage()
            img.save('samples/%s%s' % (item.itemnumber, getExt(img.format)))
        except Exception as e:
            print(e, item)

    def preSelection(self, item, search, ratio):
        print(search.hostLocation(), ratio)
        return ratio

    def testSelection(self, item):
        if item.reason.ratio > 0:
            return True
        return False

def toItem(mnfrow):
    item = searchobjects.SearchItem()
    item.marketplace = 'Wolverine'
    item.itemnumber = mnfrow['id']
    item.description = item.itemnumber
    item.brand = mnfrow['brand']
    return item

if __name__ == '__main__':
    fin = open('test.csv', 'r')
    parser = mp.ManifestParser(fin, {'brand' : 'Brand', 'id' : 'Stock Number'})

    itemset = []
    for v in parser:
        itemset.append(toItem(v))
    itemset = list(set(itemset))

    model = WolverineModel(WHITELIST)
    print('Starting', flush=True)
    SearchEngine(itemset, model, multithread=False).start()



    fin.close()



