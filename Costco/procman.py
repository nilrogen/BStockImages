"""
" procman.py
"
" This file processes the manifests. Either by being run as a script where it
" will add to the previous AllItems.json; or as a module where it has 
" functions to read the contents of that file. 
"""
from items import *
from config import _FNAME, _MANIFEST_PATH, _IMAGES_PATH

import json
import os
import csv
import sys

itemjson = None
itemlist = None

def setall():
    global itemjson, itemlist
    if itemjson == None:
        with open(_FNAME, 'r') as allitems:
            itemjson = json.load(allitems)
    if itemlist == None:
        itemlist = list(map(Item.fromJSON, itemjson['items']))
    
def getItemJson():
    setall()
    return itemjson

def getItemList():
    setall()
    return itemlist

def applyFilter(fn):    
    setall()
    return list(filter(fn, itemlist))

def getFound():
    return applyFilter(lambda item: item.found)

def getMissing():
    return applyFilter(lambda item: not item.found)

def findCols(csvin):
    # Take first item, return col of item # and description
    num, des, extret, cat = -1, -1, -1, -1
    value = next(csvin)

    for i in range(len(value)):
        elem = value[i].lower()
        if elem.find('item #') != -1 or elem == 'item' or elem == 'Costco ITEM':
            num = i
        elif elem.find('description') != -1 or elem.find('item description') != -1:
            des = i
        elif elem.find('ext. retail') != -1 or elem.find('extended price') != -1:
            extret = i
        elif elem == 'category' != -1:
            cat = i

    return num, des, extret, cat

def parseCSV(itemset, fin):
    #Find item number column
    csvin = csv.reader(fin)
    num, des, extret, cat = findCols(csvin)
    found, length = 0, 0

    if num == -1:
        raise Exception('Issue finding item number' + str(fin))
    elif des == -1:
        raise Exception('Issue finding item description')
    elif extret == -1:
        raise Exception('Issue finding Ext. Retail')

    itemsmanifest = []
    print(fin.name)
    sys.stdout.flush()

    for value in csvin:
        length += 1
        try:
            ival = int(value[num])
            item = Item(ival, value[des])
            item.extretail = value[extret]

            if cat != -1:
                item.category = value[cat]

            print(item)

            itemsmanifest.append(item)
        except Exception as e:
            print('Issue in: {} {}'.format(fin, e))
    itemsmanifest.sort(key=lambda x: x.extretail, reverse=True)

    if (len(itemsmanifest) > 1):
        assert itemsmanifest[0].extretail >= itemsmanifest[1].extretail
    manset = set(itemsmanifest[0:round(1*length)])
    itemset = itemset.update(manset)

    return found == length
    
def generateList(listpct):
    jsn = { 'processed' : False, 'count' : 0, 'found' : 0 }
    os.chdir(_MANIFEST_PATH)

    with open(_FNAME, 'w') as allitems:
        jsn = json.load(allitems)
    
    # Loop through each manifest and add each item to jsn['items']
    itemlist = set()
    for manifest in os.listdir():
        with open(manifest) as fin:
            parseCSV(itemlist, fin)

    imagelist = sorted(itemlist, key=lambda i: i.itemnum)
    for image in os.listdir(_IMAGES_PATH):
        basename, ext = os.path.splitext(image)
        for item in imagelist:
            if int(basename) == item.itemnum:
                item.found = True
                item.imagename = '{}{}'.format(basename, ext)
                jsn['found'] += 1
                break
    with open(_FNAME, 'w') as allitems:
        jsn['count'] = len(itemlist)
        jsn['processed'] = True
        jsn['items'] =  list(map(lambda itm: Item.toJSON(itm), itemlist))

        json.dump(jsn, allitems, indent=4)

#def update():
    #global itemlist, itemjson
    #missing = getMissing()
    #imgs = list(map(lambda x: os.path.splitext(x)[0]), \
                    #os.listdir(_IMAGES_PATH))

    #for item in missing:
        #if str(item.itemnum) in imgs:
        


if __name__ == '__main__':
    try:
        # Otherwise print all manifests that have items that have been found
        with open(_FNAME, 'r') as allitems:
            pass
    except FileNotFoundError:
        try:
            jsn = { 'processed' : False, 'count' : 0, 'found' : 0 }
            
            # Loop through each manifest and add each item to jsn['items']
            os.chdir(_MANIFEST_PATH)
            itemlist = set()
            for manifest in os.listdir():
                with open(manifest) as fin:
                    parseCSV(itemlist, fin)

            imagelist = sorted(itemlist, key=lambda i: i.itemnum)
            for image in os.listdir(_IMAGES_PATH):
                basename, ext = os.path.splitext(image)
                for item in imagelist:
                    if int(basename) == item.itemnum:
                        item.found = True
                        item.imagename = '{}{}'.format(basename, ext)
                        jsn['found'] += 1
                        break

            with open(_FNAME, 'w') as allitems:
                jsn['count'] = len(itemlist)
                jsn['processed'] = True
                jsn['items'] =  list(map(lambda itm: Item.toJSON(itm), itemlist))

                json.dump(jsn, allitems, indent=4)
        except IOError as e:
            print(type(e), e.args)
