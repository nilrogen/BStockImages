import sys, os
sys.path.append(os.getenv('home'))

import BStockImages.util.manifestparser as mp
from BStockImages.util.db.dbmongo import getClient
from BStockImages.util.images import download_image

from html.parser import HTMLParser

import requests as rq

class GEParser(HTMLParser):
    def __init__(self):
        super().__init__() 
        self.found = False
        self.url = ''
        self.state = 0

    def handle_starttag(self, tag, attrs):
        if self.state == 0 and tag == 'a' and \
            ('class','image-scroller-image active-image') in attrs:
            self.state = 1
        elif self.state == 1 and tag == 'img':
            for k,v in attrs:
                if k == 'src':
                    self.url = v
            self.state = 2
            self.found = True


def searchGE(modelnum):
    URL = 'http://products.geappliances.com/appliance/gea-specs/%s'
    HEADER = { 'User-Agent' : 'Mozilla/5.0' }

    print(modelnum, flush=True)
    parse = GEParser()

    retv = None
    with rq.get(URL % modelnum, headers=HEADER) as req:
        print(req.status_code)
        if req.status_code == 200:
            parse.feed(req.text)
            if parse.found:
                retv = parse.url
    return retv
    
GED = {
    'modelnumber' : 'MODEL'
}


if __name__ == '__main__':
    count = 0
    with open('master.csv', 'r')  as fin:
        mpl = mp.ManifestParser(fin, GED)    
        for elm in mpl:
            mn = elm['modelnumber'] 
            url = searchGE(mn)
           
            if url == None:
                count += 1
                print(count)
                continue
            print('Downloading ',mn, flush=True)
            img = download_image(url)
            if img == None:
                print('Doesnt Exists!')
                continue
            img.save('images/%s.jpg' % str(mn))
            sys.stdout.flush()
