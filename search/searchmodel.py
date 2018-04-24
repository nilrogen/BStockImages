"""
Here the model for searching for images is created.

The idea is that a minimal amount of options are user defined. The rest
works as it should.

Options are:
    1. Website checking.
    2. The whitelist / multipliers
    3. Marketplace function before choosing best
    4. Marketplace categorizer 
    5. Query options

@author Michael Gorlin
@date 2018-02-14
"""
import sys, os
sys.path.append(os.getenv('HOME'))

import BStockImages.search.searchobjects as so
import BStockImages.search.bingimage as bi

from random import randint
import threading 
import time
from fuzzywuzzy import fuzz

class SearchModel(object):
    
    def __init__(self, marketplace):
        self.marketplace = marketplace
        self.whitelist = { 'www.%s.com' % self.marketplace : 1 } 
        self.descriptionmatching = True

    def websiteCheck(self, item):
        """
        Override this method to enable website checking. Return True
        if an item is found and handle its update otherwise return false.
        """
        return False

    def checkWhitelist(self, location, ratio):
        if location in self.whitelist:
            return ratio * self.whitelist[location]
        return -1

    def queryOptions(self):
        """ Uses the SearchItem.getQuery options """
        return [ 'MBID' ]

    def preSelection(self, item, search, ratio):
        return ratio
    def postSelection(self, item):
        return True
    def saveSuccess(self, item):
        pass
    def saveFailure(self, item):
        pass
    def saveWebResult(self, item):
        pass

class SearchEngine(object):

    def __init__(self, itemlist, model, maxsearch=60, multithread=True):
        self.itemlist = itemlist
        self.model = model
        self.maxsearch = maxsearch
        self.multithread = multithread

        self.lock = threading.Lock()

    def start(self):
        for item in self.itemlist:
            if self.multithread:
                #Spawn new thread
                t = threading.Thread(target = self.threadMainFunc, \
                                     args=(item,))
                t.start()
            else: 
                self.threadMainFunc(item)
            sys.stdout.flush()

            time.sleep(1/101 * len(self.model.queryOptions()))
    
    def threadFindBestFunc(self, item, search):
        if search.valueCount() == 0:
            return

        for i in range(min(search.valueCount(), self.maxsearch)):
            value = search.getValue(i)
            # chose ratio (how good the image is) by lay            # the UQRatio, whitelist multiplyer, model specific selector
            ratio = fuzz.UQRatio(item.description, value.name())
            ratio = self.model.checkWhitelist(value.hostLocation(), ratio)
            ratio = self.model.preSelection(item, value, ratio)
            
            # Fix equal ratios by choosing one randomly
            if ratio != -1 and ratio == item.reason.ratio:
                ratio += randint(0, 1) 
            # If ratio is higher than previous 
            if ratio > item.reason.ratio:
                # Save reasons and search result
                item.reason.ratio = ratio
                item.reason.host = value.hostLocation()
                item.reason.description = value.name()
                item.reason.imglink = value.contentLink()
                item.searchresult = value
        
    def threadMainFunc(self, item):
        item.setReason(so.SearchReason(False))

        # Check Website
        if self.model.websiteCheck(item):
            item.reason.success = True
            item.reason.website = True
            self.saveWebResult(item)
        
        print('Tested Website', flush=True)
        # Test Queries
        item.reason.ratio = -1
        for qopt in self.model.queryOptions():
            query = item.getQuery(qopt)
            item.reason.query = query
            #self.lock.acquire()
            search = bi.imageSearch(query, cc='en-US')
            while search is None:
                time.sleep(.5)
                search = bi.imageSearch(query)
            
            #self.lock.release()
            # If no search results appear then save that result
            print(search.valueCount())
            if search.valueCount() == 0:
                item.reason.success = False
                item.reason.failedsearch = True
                self.model.saveFailure(item)
                return

            # Find best search result
            self.threadFindBestFunc(item, search)

        if self.model.testSelection(item):
            item.reason.success = True
            self.model.saveSuccess(item)
        else:
            self.model.saveFailure(item)
