import requests
from html.parser import HTMLParser


import PIL as pil
import PIL.Image as Image

from config import *

import sys
import time
import os

_SAVE_PATH = os.path.join(os.getenv('HOME'), 'Images')

class CostcoParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.found = False
        self.itemnum = -1
        self.pictureurl = ""

    def handle_starttag(self, tag, attrs):
        if self.found:
            return 
        if tag == 'span' and self.itemnum == -1:
            for k,v in attrs:
                if 'data-sku' == k:
                    print('Sku')
                    self.itemnum = int(v)
                    if self.pictureurl != "":
                        self.found = True
                    break
        if tag == 'img' and self.pictureurl == "":
            if ('id', 'initialProductImage') in attrs:
                for k, v in attrs:
                    if k == 'src':
                        self.pictureurl = v
                        if self.itemnum != -1:
                            self.found = True
                        break
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
    u = 'https://www.costco.com/.product.%d.html'
    header = {'User-agent': 'Mozilla/5.0'}

    start=12000000
    for i in range(0, 50000, 1):
        print('Trying %d'% (i+start))
        sys.stdout.flush()        

        req = requests.get(u % (i+start), headers=header)
        if req.status_code == 200:
            p = CostcoParser()
            p.feed(req.text)

            print('%d %s'%(p.itemnum, p.pictureurl), p.found)
            sys.stdout.flush()        
            if not p.found:
                #time.sleep(.2)
                continue

            print('Downloading Image')
            sys.stdout.flush()        
            imgreq = requests.get(p.pictureurl, stream=True, headers=header)
            if imgreq.status_code != 200:
                print('========STATUS CODE: %d========'%(imgreq.status_code))
                continue
            imgreq.raw.decode_content = True
            img = Image.open(imgreq.raw)

            p = os.path.join(_SAVE_PATH, str(p.itemnum)+getExt(img.format))
            with open(p, 'wb') as fout:
                img.save(fout)
            imgreq.close()
        req.close()
    sys.stdout.flush()        
