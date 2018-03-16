import os
import pymongo

_CLIENT = None
def _setup():
    import csv
    global _CLIENT
    
    if not _CLIENT:
        filedir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(filedir, 'keys.csv')) as fin:
            reader = csv.reader(fin)
            for name, key in reader:
                if str(name) == 'MONGOIP':
                    key = str(key)
                    _CLIENT = pymongo.MongoClient(key)

def getClient():
    _setup()
    return _CLIENT
