import os

_CLIENT = None
def _setup():
    import csv
    global _CLIENT
    
    if not _CLIENT:
        filedir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(filedir, 'keys.csv')) as fin:
            reader = csv.reader(fin)
            for name, key in reader:
                if str(name) == 'MONGOKEY':
                    key = str(key)
                    _CLIENT = MongoClient(key)

def getClient():
    _setup()
    return _CLIENT
