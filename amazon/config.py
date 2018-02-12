import sys
import os

ACCESS_KEY, SECRET_KEY = None, None

def getKeys():
    import csv
    global ACCESS_KEY, SECRET_KEY
    filedir = os.path.dirname(os.path.abspath(__file__))

    if not (ACCESS_KEY or SECRET_KEY):
        with open(os.path.join(filedir, 'keys.csv')) as fin:
            reader = csv.reader(fin)
            ACCESS_KEY = str(next(reader)[1])
            SECRET_KEY = str(next(reader)[1])
getKeys()

ADDRESS    = 'https://webservices.amazon.com/onca/xml'

__all__ = ['ADDRESS', 'ACCESS_KEY', 'SECRET_KEY']

