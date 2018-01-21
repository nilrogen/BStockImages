import sys
import os
sys.path.append(os.getenv('HOME'))

from model import *
from config import _FRIGIDAIRE_IMAGES

from BStockImages.util.manifestparser import ManifestParser

import time
import csv
import requests
import random
import webbrowser

def findColumns(csvin):
    value = next(csvin)

    mi, bi = -1, -1

    for i in range(len(value)):
        element = value[i].lower()
        
        if element.find('model number') != -1:
            mi = i
        if element == 'brand_cd':
            bi = i
    
    if mi == -1 or bi == -1:
        raise ValueError('Issue with finding index')

    return mi, bi


def parseCSV(fin):
    csvin = csv.reader(fin)
    modelset = set()
    modelindex, brandindex = findColumns(csvin)
    knownimages = list(map(lambda v: os.path.splitext(v)[0].lower(),
                           os.listdir(_FRIGIDAIRE_IMAGES)))

    for value in csvin:
        try:
            modelnumber = value[modelindex]
            model = Model(modelnumber)
            brnd = value[brandindex]
            if brnd == 'M':
                if modelnumber.lower() in knownimages:
                    model.found = True
                modelset.add(model)
        except Exception as e:
            print('Issue in: {} {}'.format(fin, e))
    
    return modelset


def generateList():
    with open('Elec-Frig Model DB.csv', 'r') as fin:
        modelset = parseCSV(fin) 
    return list(modelset)
            
if __name__ == '__main__':
    CDICT = { 'model-number' : 'Model Number', 'cf' : 'BRAND_CD' }
    with open('Elec-Frig Model DB.csv', 'r') as fin:
        mp = ManifestParser(fin, CDICT)
        for i in mp:
            print(i)
            break

    #lst = generateList()

    #linkstr = 'https://www.frigidaire.com/Kitchen-Appliances/Refrigerators/French-Door-Refrigerator/{}/'

    #for i in range(10):
    #    webbrowser.open(linkstr.format(lst[random.randint(0, len(lst))]))      
    #    time.sleep(.5)

