import config

from BStockImages.search import *
from BStockImages.search.searchmodel import *
import BStockImages.util.db.dbmongo as dbm
import BStockImages.util.manifestparser as mp

WHITELIST = { 
   'www.amazon.com' :   1,
   'www.amazon.co.uk' : 1,
   'www.amazon.de' :    1
}

_SAVE_PATH = os.path.join(os.path.join(os.getenv('HOME'), 'Images', 'Amazon'))

def getExt(s):
    if s == None:
        raise ValueError
    elif s == 'JPEG':
        return '.jpg'
    elif s == 'PNG':
        return '.png'
    else:
        return '.jpg'

class AmazonItem(searchobjects.SearchItem):
    def __init__(self):
        super(AmazonItem, self).__init__()
        self.countrycode = 'en'
    
    def getSearchOption(self, value):
        if value == 'C':
            return self.countrycode
        return super(AmazonItem, self).getSearchOption(value)

class AmazonModel(SearchModel):
    def __init__(self, marketplace, dbtbl, whitelist):
        super(AmazonModel, self).__init__(marketplace)
        self.whitelist = WHITELIST
        self.whitelist[marketplace] += .2
        self.dbtbl = dbtbl
    
    def queryOptions(self):
        return [ 'MCD' ]

    def save(self, item):
        query = [
            { 'asin' : item.itemnumber },
            { '$set' : { 'searched' : True,
                         'found' : item.reason.success,
                         'reasons' : item.reason.toJSON() }}
        ]
        self.dbtbl.find_one_and_update(query[0], query[1])

    def saveFailure(self, item):
        print('-', end='')
        #self.save(item)
    
    def saveSuccess(self, item):
        try:
            print(item.reason.host, item.reason.ratio)
            img = item.searchresult.downloadImage()
            p = os.path.join(_SAVE_PATH, str(item.itemnumber)+getExt(img.format))
            with open(p, 'wb') as fout:
                img.save(fout)
                #self.save(item)
        except Exception as e:
            print(e, item)
        print('+', end='')

    def preSelection(self, item, search, ratio):
        return ratio

    def testSelection(self, item):
        return item.reason.ratio != -1

def toItem(asin, desc, countrycode='en'):
    item = AmazonItem()
    item.countrycode = countrycode
    item.description = desc
    item.itemnumber = asin

    return item

if __name__ == '__main__':
    azmm = { 'asin' : 'asin', 'desc' : 'Item Name' }  
    
    items = []
    with open('AZDE_OV_TL_03012018.csv', 'r') as fin:
        mpl = mp.ManifestParser(fin, azmm)
        for azi in mpl:
            asin = azi['asin']
            des = azi['desc']

            if not asin or not des:
                continue
            items.append(toItem(asin, des, 'de'))

    model = AmazonModel('www.amazon.de', None, WHITELIST)
    SearchEngine(items, model).start()
