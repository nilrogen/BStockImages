import time
import requests 
import json
import sys
import os

import PIL as pil
import PIL.Image as Image

from random import shuffle
from urllib.parse import urlsplit
from fuzzywuzzy import fuzz

sys.path.append(os.getenv('HOME'))
import BStockImages.search.bingimage as bi
import procman as pm

_SAVE_PATH = os.path.join(os.getenv('HOME'), 'Images')

blacklist = [ 'www.cochaser.com', \
              'www.frugalhotspot.com' ]

whitelist = [ ('www.costco.com', 1.2), \
              ('www.costcobusinessdelivery.com', 1.2), \
              ('www.costco.co.uk', 1.15), \
              ('www.costco.ca', 1.15), \
              ('www.amazon.com', 1.1), \
              ('amazon.com', 1.1), \
              ('amazon.co.uk', 1.1), \
              ('www.homedepo.com', 1), \
              ('www.walmart.com', 1), \
              ('www.samsclub.com', 1), \
              ('www.target.com', 1), \
              ('www.kohls.com', 1), \
              ('www.instacart.com', 1), \
              ('www.bjs.com', .9), \
              ('www.walgreens.com', .9), \
              ('www.sears.com', .9), \
              ('www.overstock.com', .9), \
              ('www.ebay.com', .4) ]

def getPriority(item, value):
    retv = fuzz.UQRatio(item.description, value.name())
    wl = False

    host = value.hostLocation()

    if host in blacklist:
        return -1

    # Loop through whitelist and if host matches multiply return value by priority factor
    for i in range(len(whitelist)):
        if host == whitelist[i][0]:
            retv = round(whitelist[i][1] * retv)
            wl = True

    """
    try:
        print("\nDescription: {}\nValue: {}\nQRatio: {}\nWRatio: {}\n".format( \
            item.description, value.name(), retv, \
            fuzz.UWRatio(item.description, value.name())))
    except:
        pass
"""
    if retv < 50:
        return -1

    if not wl:  
        return -1
    return retv

def formatQueries(itm):
    return ["Costco %d %s" % (itm.itemnum, item.description), \
            item.description ]

def findBestPicture(item, bingres):
    topres = (-1, None)

    if bingres.valueCount() == 0:
        return topres
    for i in range(bingres.valueCount()):
        if i == 60:
            break
        imageresult = bingres.getValue(i)
        pri = getPriority(item, imageresult)
        if topres[0] < pri:
            topres = (pri, imageresult)

    return topres

def getExt(s):
    if s == None:
        raise ValueError
    elif s == 'JPEG':
        return '.jpg'
    elif s == 'PNG':
        return '.png'
    else:
        return '.jpg'

def outputString(item, topres):
    """
    " Format of output:
    " description, result name, uqratio, hostlocation, 
    """
    items = "{} {}"

if __name__ == '__main__':
    # Need to change user agent in order for costco cdn to accept requests 
    HEADERS = {'User-agent': 'Mozilla/5.0'}

    # Generate set of Items 
    itemlist = pm.getMissing()

    print(len(itemlist), flush = True)
    shuffle(itemlist)

    avg = 0
    ln  = len(itemlist)
    sm  = 0 
    cnt = 0

    vals = [ 0, 0 ] 

    for i in range(ln):
        # take first item
        item = itemlist[i] 

        best = (-1, None)
        fi, j = 0, 0
        # Get search data 
        try:
            for query in formatQueries(item):
                searchreq = bi.imageSearch(query)
                # Find best image among results
                pri, image = findBestPicture(item, searchreq)

                if pri > best[0]:
                    fi = j
                    best = (pri, image)
                j += 1

            if best[1] == None:
                pm.update(item)
                print('-', flush=True, end='')
                sm += 1
                continue
        except KeyError as e:
            print(e, type(e))
            continue
        except UnicodeEncodeError as e:
            print(e, type(e))
            continue
        except Exception as e:
            print(e, type(e), query)
            continue

        vals[fi] += 1
        avg = cnt/(cnt+1) * avg + sm/(cnt+1) 
        cnt += 1
        sm = 0
        print(' < %d / %d | %.2f ' % (cnt, i, avg), end='', flush=True)
        print(' | {} - {} >'.format(fi, vals), flush=True)

        # Retreive results
        with requests.get(best[1].contentLink(), stream=True, headers=HEADERS, verify=False) as imgreq:
            if imgreq.status_code != 200:
                continue
            imgreq.raw.decode_content = True
            img = Image.open(imgreq.raw)

            p = os.path.join(_SAVE_PATH, str(item.itemnum)+getExt(img.format))
            with open(p, 'wb') as fout:
                try:
                    img.save(fout)
                except OSError as e:
                    print(e, fout)
                    continue

            fmt = '{:<10} {}  |  {}  |  {}  |  {}'.format( \
                    item.itemnum, best[0], item.description, \
                    best[1].name(), best[1].hostLocation())
            print(fmt)
            sys.stdout.flush()

            pm.update(item)

            with open(os.path.join(_SAVE_PATH, 'output.txt'), 'a') as fout:
                fout.write(fmt)
