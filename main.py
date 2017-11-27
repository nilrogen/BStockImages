import os
import requests 
import json

import PIL as pil
import PIL.Image as Image

from random import shuffle
from urllib.parse import urlsplit
from fuzzywuzzy import fuzz

import bingimage as bi
import procman as pm

_SAVE_PATH = os.path.join(os.getenv('HOME'), 'Images')

blacklist = [ 'www.cochaser.com', \
              'www.frugalhotspot.com' ]
whitelist = [ ('www.costco.com', 1.5), \
              ('www.costcobusinessdelivery.com', 1.4), \
              ('www.amazon.com', 1.25), \
              ('www.homedepo.com', 1), \
              ('www.ebay.com', .75), \
              ('www.walmart.com', 1), \
              ('www.samsclub.com', 1), \
              ('www.costco.co.uk', 1.4), \
              ('www.kohls.com', 1) ]

def getPriority(item, value):
    retv = fuzz.UQRatio(item.description, value.name())
    wl = False

    host = value.hostLocation()
    print(host, retv)

    if host in blacklist:
        return -1

    # Loop through whitelist and if host matches multiply return value by priority factor
    for i in range(len(whitelist)):
        if host == whitelist[i][0]:
            retv = round(whitelist[i][1] * retv)
            wl = True

    try:
        print("\nDescription: {}\nValue: {}\nQRatio: {}\nWRatio: {}\n".format( \
            item.description, value.name(), retv, \
            fuzz.UWRatio(item.description, value.name())))
    except:
        pass

    if not wl:  
        return -1
    return retv

def formatQuery(itm):
    return "Costco %d %s" % (itm.itemnum, item.description)

def findBestPicture(item, bingres):
    if bingres.valueCount() == 0:
        return None
    
    topres = (-1, None)

    for i in range(bingres.valueCount()):
        if i == 20:
            break
        imageresult = bingres.getValue(i)
        pri = getPriority(item, imageresult)
        if topres[0] < pri:
            topres = (pri, imageresult)


    if topres[1] is not None:
        print('*********\nBest: {} {}\n*********'.format(topres[0], topres[1].hostLocation()))
    return topres[1]

def getExt(s):
    if s == None:
        raise ValueError
    elif s == 'JPEG':
        return '.jpg'
    elif s == 'PNG':
        return '.png'
    else:
        return '.jpg'

if __name__ == '__main__':
    # Need to change user agent in order for costco cdn to accept requests 
    HEADERS = {'User-agent': 'Mozilla/5.0'}

    # Generate set of Items 
    itemlist = pm.getMissing()
    shuffle(itemlist)

    for i in range(len(itemlist)):
        # take first item
        item = itemlist[i] 

        # Get search data 
        try:
            searchreq = bi.imageSearch(formatQuery(item))

            # Find best image among results
            image = findBestPicture(item, searchreq)
            if image == None:
                continue
        except KeyError as e:
            print(e)
            continue
        except UnicodeEncodeError as e:
            print(e)
            continue

        # Retreive results
        with requests.get(image.contentLink(), stream=True, headers=HEADERS) as imgreq:
            if imgreq.status_code != 200:
                continue
            imgreq.raw.decode_content = True
            img = Image.open(imgreq.raw)

            p = os.path.join(_SAVE_PATH, str(item.itemnum)+getExt(img.format))
            with open(p, 'wb') as fout:
                img.save(fout)

            with open(os.path.join(_SAVE_PATH, 'output.txt'), 'a') as fout:
                fout.write(str(item)+' {} {}\r\n'.format( \
                        image.name(), image.hostLocation()))
