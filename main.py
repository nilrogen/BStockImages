import json
import os
import sys
import requests
import shutil

from random import shuffle

import googleimage as gi
import procman as pm

_SAVE_PATH = os.path.join(os.getenv('HOME'), 'Images')

class searchResult:
    def __init__(self, item, jsn):
        self.item = item
        self.mime = jsn['mime']
        self.ext = self.mime.split('/')[1]
        if self.ext == 'jpeg':
            self.ext = 'jpg'

        self.link = jsn['link'].strip()
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
    
    count = int(jsn['searchInformation']['totalResults'])
    if count == 0:
        return None

    results = jsn['items']
    pres = []
    for i in range(count):
        res = searchResult(item, results[i])
        res.setPriority(i)
        pres.append(res)

    if pres[0].priority == -1:
        return None
    return pres[0]
    



if __name__ == '__main__':
    # Generate set of Items 
    print('hello')

    itemlist = pm.getMissing()

    shuffle(itemlist)

    print(requests.get('http://google.com'))

    for i in range(1):
        item = itemlist[i] 
        #req = gi.imageSearch(formatQuery(item))


        jsn = json.load(open(os.path.join(_SAVE_PATH, 'output.json')))
        #if jsn['searchInformation']['totalResults'] != '0':
           #json.dump(jsn, open(os.path.join(_SAVE_PATH, 'output.json'), 'w'), indent=4)
        #req.close()

        res = findPictures(item, jsn)
        print(res)

        print(item)
        if res is not None:
            print(formatQuery(item))
            print(res.link)

            sys.stdout.flush()
            r = requests.get(res.link, stream=True)
            if r.status_code == 200:
                path = os.path.join(_SAVE_PATH, res.getName())
                with open(path, 'wb') as fout:
                    r.raw.decoce_content = True
                    shutil.copyfileobj(r.raw, fout)
