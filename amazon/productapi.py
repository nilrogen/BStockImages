from config import *

from lxml import objectify, etree

import bottlenose as bn

REGIONS = {
    'US' : 'nilrogen-20', 
    'UK' : 'nilrogen-21', 
    'ES' : 'nilrogen0c-21',
    'FR' : 'nilrogen07-21',
    'DE' : 'nilrogen08-21'
}

class AmazonItem(object):
    def __init__(self, lookup):
        self.root = objectify.fromstring(lookup)
        try:
            self.error = self.root.Items.Request.Errors.Error
            print(repr(self.error))
        except:
            self.item = self.root.Items.Item

    def getImage(self):
        if self.error:
            print(self.item.ImageSets.ImageSet.LargeImage.URL)
            return str(self.item.ImageSets.ImageSet.LargeImage.URL)
        return None
        


class ItemLookup(object):
    def __init__(self, cc='US'):
        self.amzn = bn.Amazon(ACCESS_KEY, SECRET_KEY, REGIONS[cc], 
                              Region=cc, MaxQPS=0.9)
    
    def _lookup(self, **kwargs):
        lookup = None
        try:
            if not kwargs.get('ResponseGroup'):
                kwargs['ResponseGroup'] = 'Images,ItemAttributes'
            lookup = self.amzn.ItemLookup(**kwargs)
            itm = AmazonItem(lookup)

            return itm
        except Exception as e:
            print(e)
            return lookup

    def lookupASIN(self, asin, **kwargs):
        return self._lookup(ItemType='ASIN', ItemId=asin, **kwargs)

    def lookupSKU(self, sku, **kwargs):
        return self._lookup(ItemType='SKU', ItemId=sku, **kwargs)

    def lookupUPC(self, upc, **kwargs):
        return self._lookup(ItemType='UPC', ItemId=upc, **kwargs)

if __name__ == '__main__':
    lu = ItemLookup()
    val = lu.lookupASIN('B01JGOMR6K') 


