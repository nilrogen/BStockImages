import json
import os
import urllib

from random import shuffle

import googleimage as gi
import countfiles as cf

_PATH_IMAGES = 'C:\Users\Mike Work\Desktop\TestImage'
_VALID_EXT = [ 'jpg', 'png' ]

class searchResult:
    def __init__(self, item, jsn):
        self.item = item
        self.mime = jsn['mime']
        self.ext = self.mime.split('/')[1]
        if self.ext == 'jpeg':
            self.ext = 'jpg'

        self.link = jsn['link']
        self.displaylink = jsn['displayLink']
        self.priority = -1

    def __cmp__(self, other):
        return self.priority - other.priority

    def __str__(self):
        return "%s - %s\n" % (self.link, self.priority)

    def __repr__(self):
        return str(self)

    def setPriority(self, index):
        """
        " For each result check if it's a valid image (jpeg, png).
        " Evaluate where the result is from and determine its priority.
        " Images from Costco are the highest in the order they appear
        " in the search results. Next are Amazon's results. 
        "
        " @arg res - An element in the list jsn['items']
        " @arg index - Which element in the results list this is.
        " @return The priority of the image result (higher is a better result)
        """
        # check if valid image result
        if self.ext in _VALID_EXT:
            if self.displaylink == 'www.costco.com':
                self.priority =  1000 - index
            elif self.displaylink == 'www.amazon.com':
                self.priority = 100 - index
            else:
                self.priority = 1000 - index

    def getName(self):
        return "%s.%s" % (self.item.itemnum, self.ext)

def formatQuery(itm):
    return "Costco %d %s" % (itm.itemnum, item.description)


def findPictures(items, jsn):
    """
    " Find the picture in returned search results
    "
    "
    " Helpful items
    " jsn['items']                   - List of search results
    " jsn['items'][i]                - An item in the results
    " jsn['items'][i]['displayLink'] - The base website of image (www.costco.com)
    " jsn['items'][i]['link']        - The link for the image
    " jsn['items'][i]['mime']        - The type of image (image/jpeg)
    "
    " jsn['searchInformation']['totalResults'] - Number of results
    "
    " @arg jsn - The returned search results of a google image search
    " @arg item - The item that is being found
    " @return The url of the item if found, None if not
    """
    
    cnt = int(jsn['searchInformation']['totalResults'])
    if cnt == 0:
        return None

    results = jsn['items']
    pres = []
    for i in range(len(results)):
        res = searchResult(item, results[i])
        res.setPriority(i)
        pres.append(res)

    pres.sort(reverse = True) 

    if pres[0].priority == -1:
        return None
    return pres[0]
    


if __name__ == '__main__':
    # Generate set of Items 

    """
    itemlist = list(cf.generateSet())

    shuffle(itemlist)

    for i in range(40):
        item = itemlist[i] 
        req = gi.imageSearch(formatQuery(item))

        jsn = json.loads(req.content)
        req.close()

        res = findPictures(item, jsn)

        print item
        if res is not None:
            print formatQuery(item)
            urllib.urlretrieve(res.link, os.path.join(_PATH_IMAGES, res.getName()))


    """
