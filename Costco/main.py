import config

from BStockImages.search.searchmodel import *
from BStockImages.search import *
import BStockImages.util.db.dbmongo

from random import shuffle

import pymongo
_SAVE_PATH = os.path.join(os.getenv('HOME'), 'Images')

WHITELIST = { 'www.costco.com'                 : 1.2,  \
              'www.costcobusinessdelivery.com' : 1.2,  \
              'www.costco.co.uk'               : 1.15, \
              'www.costco.ca'                  : 1.15, \
              'www.amazon.com'                 : 1.1,  \
              'amazon.com'                     : 1.1,  \
              'amazon.co.uk'                   : 1.1,  \
              'www.homedepo.com'               : 1,    \
              'www.walmart.com'                : 1,    \
              'www.samsclub.com'               : 1,    \
              'www.target.com'                 : 1,    \
              'www.kohls.com'                  : 1,    \
              'www.instacart.com'              : 1,    \
              'www.bjs.com'                    : .9,   \
              'www.walgreens.com'              : .9,   \
              'www.sears.com'                  : .9,   \
              'www.overstock.com'              : .9,   \
              'www.ebay.com'                   : .4 }

def getExt(s):
    if s == None:
        raise ValueError
    elif s == 'JPEG':
        return '.jpg'
    elif s == 'PNG':
        return '.png'
    else:
        return '.jpg'


class CostcoModel(SearchModel):
    def __init__(self, dbtbl, whitelist):
        super(CostcoModel, self).__init__('Costco')
        self.whitelist = whitelist

        self.dbtbl = dbtbl
    
    def queryOptions(self):
        return [ 'MID', 'D' ] 


    def save(self, item):
        self.dbtbl.find_one_and_update( \
            { 'item-num' : item.itemnumber }, \
            { '$set' : { 'searched' : True, \
                         'found' : item.reason.success, \
                         'reasons' : item.reason.toJSON() }})

    def saveFailure(self, item):
        print('-', end='')
        self.save(item)
        
    def saveSuccess(self, item):
        try:
            img = item.searchresult.downloadImage()
            p = os.path.join(_SAVE_PATH, str(item.itemnumber)+getExt(img.format))
            with open(p, 'wb') as fout:
                    img.save(fout)
                    self.save(item)
        except Exception as e:
            print(e, item)

        print('+', end='')


    def preSelection(self, item, search, ratio):
        return ratio
    
    def testSelection(self, item):
        if item.reason.ratio > 50:
            return True
        return False
        
def toItem(ccitem):
    item = searchobjects.SearchItem()
    item.marketplace = 'costco'
    item.itemnumber = ccitem['item-num']
    item.brand = ''
    item.description = ccitem['description']
    item.loadReason(ccitem['reason'])

    return item
    
    

if __name__ == '__main__':
    client = pymongo.MongoClient('192.168.1.13')
    db = client.Items
    col = db.costco

    items = col.find({'searched' : False, 'found' : False})
    fitem = col.find({'found' : True})

    print('Found:              ', len(list(fitem)))
    print('Remaining Items:    ', len(list(items)))
    print('Total Items:        ', len(list(col.find())))

    """
    searchitems = list(map(toItem, items))
    shuffle(searchitems)

    model = CostcoModel(col, WHITELIST)
    print('Starting Engine', flush=True)
    SearchEngine(searchitems, model).start()
    print('Done', flush=True)
    """ 
