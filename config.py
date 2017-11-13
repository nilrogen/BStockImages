import sys
import os
import json

def getDropboxPath():
    # Gets the Dropbox path depending on the platform
    fin = None
    if sys.platform == 'linux':
        fin = open(os.path.join(os.getenv('HOME'), '.dropbox/info.json'))
    if sys.platform == 'win32' or sys.platform == 'cygwin':
        fin = open(os.path.join(os.getenv('LOCALAPPDATA'), 'Dropbox\info.json'))
    else: # sys.platform == 'linux':
        fin = open(os.path.join(os.getenv('HOME'), '.dropbox/info.json'))
        
    jsn = json.load(fin)
    fin.close()

    return jsn['personal']['path']

_DROPBOX = os.path.join(getDropboxPath(), 'Marketplace Images')
_MANIFEST_PATH = os.path.join(_DROPBOX, 'Costco Manifest')
_IMAGES_PATH = os.path.join(_DROPBOX, 'Costco Images')
_FNAME = os.path.join(_MANIFEST_PATH, 'AllFiles.json')


if __name__ == '__main__':
   print(os.listdir(_IMAGES_PATH)) 
