import procman as pm
from items import *
from itemlinkedlist import *
from config import _IMAGES_PATH

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

def copyImage(base, cpy):
    base, ext = base.imagename
    copyfile(os.path.join(_IMAGES_PATH, base.imagename), \
             os.path.join(_SAVE_PATH, str(cpy.itemnum)+ext))

if __name__ == '__main__':

    # Generate Set of all items and place in linkedlist
    itemlist = ItemLinkedList()
    gs = pm.getItemList()
    random.shuffle(gs)

    # Add all images to the linked list
    for item in gs:
        itemlist.add(item)

    # List of item Groupings
    grouplist = list()
    removal = 0
    l = len(itemlist)
    # Loop through itemlist until all images have either been found or grouped.
    while len(itemlist) > 0:
        cmpitem = itemlist.pop().value
        ival = itemlist.head
        similarlist = [cmpitem]
        print(cmpitem)

        # Compare item with all other items
        # if the qratio of the descriptions is >= _ADD_RATIO (85%) 
        # we remove that item and add it to the similar group of the
        # item we are looking at
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
                    copyImage(similarlist[0], item)
                    removal += 1
    print(removal)
