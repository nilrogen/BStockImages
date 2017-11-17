import csv
import os
import os.path as path
import copy
import sys

import config

from items import *

def findCols(csvin):
    # Take first item, return col of item # and description
    num, des, extret = 0, 0, 0
    value = next(csvin)

    for i in range(len(value)):
        if value[i].find('Costco Item #') != -1:
            num = i
        elif value[i].find('Description') != -1:
            des = i
        elif value[i].find('Ext. Retail') != -1:
            extret = i
    return num, des, extret
    
"""
" Parses the manifest that is found in file fin. Adds all items to
" the itemset. Duplicates are handled by the type of ItemContainer
" itemset is.
"
" @arg itemset - An ItemContainer instance that will contain each Item 
"   in this file
" @arg fin - The file to parse (a manifest)
" @return - True if all items found in the manifest were already in the
"   itemset
"""
def parseCSV(itemset, fin):
    #Find item number column
    csvin = csv.reader(fin)
    num, des, extret = findCols(csvin)
    found, length = 0, 0

    if extret == 0:
        raise Exception('Issue finding Ext. Retail')

    itemsmanifest = []

    for value in csvin:
        length += 1
        try:
            ival = int(value[num])
            item = Item(ival, value[des])
            item.extretail = value[extret]

            itemsmanifest.append(item)
        except Exception as e:
            print('Issue in: {} {}'.format(fin, e))
    itemsmanifest.sort(key=lambda x: x.extretail, reverse=True)

    assert itemsmanifest[0].extretail >= itemsmanifest[1].extretail
    manset = set(itemsmanifest[0:round(.1*length)])
    itemset = itemset.update(manset)

    return found == length
            
def removeFileType(fname):
    return os.path.splitext(os.path.basename(fname))[0]

def eliminateFound(itemset, imagelist):
    newset = copy.deepcopy(itemset)
    for item in newset:
        if item.itemnum in imagelist:
            itemset.remove(item)

def markFound(itemlist, imagelist):
    for item in itemlist:
        if item.itemnum in imagelist:
            item.found = True


"""
" Parses all files found in the _MANIFEST_PATH constant except the
" value of _FNAME.
" 
" @arg itemlist - an ItemContainer instance
"""
def parseAll(itemlist):
    files = map(lambda p: path.join(config._MANIFEST_PATH, p), os.listdir(config._MANIFEST_PATH))

    for filepath in files: 
        if filepath == 'AllFiles.csv':
            continue
        fin = open(filepath)
        rv = parseCSV(itemlist, fin)
        fin.close()

        if rv:
            print(filepath)
            
"""
" Generates an ItemSet of all unique items found in the manifests.
" Either marks all items that have been found or removes them entirely.
" Default is to remove found images
"
" @arg markfound - (default False) whether to mark found items or remove them
"""
def generateSet(markfound=False):
    images = list(map(lambda f: int(removeFileType(f)), os.listdir(config._IMAGES_PATH)))
    itemset = ItemSet()

    parseAll(itemset)

    if markfound:
        markFound(itemset, images)
    else:
        print(len(itemset))
        eliminateFound(itemset, images)
        print(len(itemset))

    return itemset
    
"""
" Main Generates the AllFiles.csv default or if argument is generate
"""
if __name__ == '__main__':
    if len(sys.argv) == 1 or sys.argv[1] == 'generate':
        itemset = generateSet(True)

        fout = open(_FNAME, 'w')
        fout.write("Item #,Description,found,basename\n")
        for value in itemset.sort():
            fout.write(str(value))
        fout.close()
