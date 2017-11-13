import countfiles as cf
from items import *
from test import *


import os
import random 
from shutil import copyfile
from fuzzywuzzy import fuzz
from copy import deepcopy

"""
" General Algorithm:
"   Generate a list of all unique Items
"   Cluster items into groups based on levenshtein distance of description
"   For each group of size > 1
"       if at least 1 item has been found
"           create image for all unfound items in group
"""

_ADD_RATIO = 85
_IMAGES = os.listdir(_IMAGES_PATH)

def copyImage(imgmap, base, cpy):
    base, ext = imgmap[base.itemnum]
    copyfile(os.path.join(cf._IMAGES_PATH, base+ext), \
             os.path.join(_SAVE_PATH, str(cpy.itemnum)+ext))
    
    


if __name__ == '__main__':

    # Generate Set of all items and place in linkedlist
    itemlist = ItemLinkedList()
    gs = list(cf.generateSet(True))
    random.shuffle(gs)
    imgmap = {}

    for item in gs:
        itemlist.add(item)
        if item.found:
            for img in _IMAGES:
                base, ext = os.path.splitext(os.path.basename(img))
                if int(base) == item.itemnum:
                    imgmap[item.itemnum] = (base, ext)

    # List of item Groupings
    grouplist = list()
    removal = 0
    l = len(itemlist)
    while len(itemlist) > 0:
        cmpitem = itemlist.pop().value
        ival = itemlist.head
        similarlist = [cmpitem]
        print(cmpitem)

        while ival != None:
            item = ival.value
            qr = fuzz.QRatio(cmpitem.description, item.description)

            if qr >= _ADD_RATIO:
                if item.found == False:
                    removal += 1
                itemlist.remove(ival)
                similarlist.append(item)
                print('{} {}'.format(repr(ival.value), qr))
            ival = ival.next

        if len(similarlist) > 1:
            grouplist.append(similarlist)

        print(len(itemlist))

    for similarlist in grouplist:
        similarlist.sort(key=lambda i: i.found, reverse=True)
        if similarlist[0].found:
            for item in similarlist:
                if not item.found:
                    copyImage(imgmap, similarlist[0], item)
                    removal += 1
    print(removal)
