"""
" This file pulls item information from amazon associates.
" It has objects to search for items based on UPC. SKU, and ASIN.
"
" This file uses two third party libraries:
"   bottlenose - to query amazon associates
"   lxml - to parse the query results
" 
" Author: Michael Gorlin
"""
from config import *

from lxml import objectify, etree
import bottlenose as bn

# The values of this dictionary should be the amazon associates id.
REGIONS = {
    'US' : '',
    'UK' : '', 
    'ES' : '',
    'FR' : '',
    'DE' : ''
}
        
class AmazonItem(object):
    """
    " This class defines the results for each lookup. Right now it only has
    " methods to get the item's image. 
    """
    def __init__(self, lookup):
        self.root = objectify.fromstring(lookup)
        try:
            self.error = self.root.Items.Request.Errors.Error
            self.haserror = True
            print(repr(self.error))
        except:
            self.item = self.root.Items.Item
            self.haserror = False

    def getImage(self):
        if not self.haserror:
            try:
                print(self.item.ImageSets.ImageSet.LargeImage.URL)
                return str(self.item.ImageSets.ImageSet.LargeImage.URL)
            except:
                self.haserror = True
        return None

class ItemLookup(object):
    """
    " This class has methods to lookup items from the specified region.
    """
    def __init__(self, cc='US'):
        self.amzn = bn.Amazon(ACCESS_KEY, SECRET_KEY, REGIONS[cc], 
                              Region=cc, MaxQPS=0.9)
    
    def _lookup(self, **kwargs):
        lookup = None
        try:
            if not kwargs.get('ResponseGroup'):
                kwargs['ResponseGroup'] = 'Images,ItemAttributes'
            lookup = self.amzn.ItemLookup(**kwargs)

            #with open('output.xml','wb') as fout:
            #    fout.write(etree.tostring(etree.XML(lookup), pretty_print=True))
            itm = AmazonItem(lookup)

            return itm
        except Exception as e:
            print(e, type(e))
            return lookup

    def lookupASIN(self, asin, **kwargs):
        return self._lookup(ItemType='ASIN', ItemId=asin, **kwargs)

    def lookupSKU(self, sku, **kwargs):
        return self._lookup(ItemType='SKU', ItemId=sku, **kwargs)

    def lookupUPC(self, upc, **kwargs):
        return self._lookup(ItemType='UPC', ItemId=upc, **kwargs)

if __name__ == '__main__':
    lu = ItemLookup()
    val = lu.lookupASIN('B01JGOMR546K') 


