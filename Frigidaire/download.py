from model import *
from config import _IMAGES_TMP

import requests
import os
import json
import sys

import PIL as pil
import PIL.Image as Image

_OUTSTRING = 'Downloading {:<10} - {:>3}/{:>3}'

def getExt(s):
    if s == None:
        raise ValueError
    elif s == 'JPEG':
        return '.jpg'
    elif s == 'PNG':
        return '.png'
    return '.jpg'

def download_image(model):
    HEAD = { 'User-agent' : 'Mozilla/5.0' }
    try:
        with requests.get(model.imagesrc, stream=True, headers=HEAD) as req:
            if req.status_code != 200:
                print('Issue with %s at %s'%(model.modelnumber, model.imagesrc))
            req.raw.decode_content = True
            img = Image.open(req.raw)

        p = os.path.join(_IMAGES_TMP, model.modelnumber+getExt(img.format))
        with open(p, 'wb') as fout:
            img.save(fout)

    except OSError as e:
        print(e)
    except Exception as e:
        print(type(e), e, model)

if __name__ == '__main__':
    with open('Multiflex.json', 'r') as fin:
        jsn = json.load(fin)

    imglst = list(filter(lambda m: m.found and m.imagesrc != '',
                         map(Model.fromJSON, jsn['model-list'])))

    lenlst = len(imglst)
    for i in range(lenlst):
        model = imglst[i]
        print(_OUTSTRING.format(model.modelnumber, i, lenlst), end='')
        sys.stdout.flush()
        download_image(model)
        print(' Done')
        sys.stdout.flush()

