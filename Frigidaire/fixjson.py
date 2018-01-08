import json

from model import *

if __name__ == '__main__':
    with open('Multiflex.json', 'r') as fin:
        jsn = json.load(fin)
    lst = list(map(Model.fromJSON, jsn['model-list']))
    for m in lst:
        if m.imagesrc == 'https:':
            m.found = False
            m.imagesrc = ''
    jsn['model-list'] = list(map(Model.toJSON, lst))
    jsn['found-items'] = len(list(filter(lambda m: m.found, lst)))
                
    with open('Multiflex2.json', 'w') as fout:
        json.dump(jsn, fout, indent=4)
        
