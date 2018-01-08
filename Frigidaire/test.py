from model import *

import requests
import json


if __name__ == '__main__':
    
    with open('Multiflex.json', 'r') as fin:
        mjson = json.load(fin)
        mlist = list(map(Model.fromJSON, mjson['model-list']))
        mtot = int(mjson['total-items'])
        mfound = int(mjson['found-items'])

    with open('AllModels-bak.json', 'r') as fin:
        gjson = json.load(fin)
        glist = list(map(Model.fromJSON, gjson['model-list']))
        gtot = int(gjson['total-items'])
        gfound = int(gjson['found-items'])

    etot = mtot + gtot
    efound = mfound + gfound
    elist = mlist + glist

    with open('AllModels.json', 'w') as fout:
        elist = list(map(Model.toJSON, elist))
        ejson = { 'total-items' : etot, 
                  'found-items' : efound, 
                  'model-list'  : elist } 
        json.dump(ejson, fout, indent=4)
