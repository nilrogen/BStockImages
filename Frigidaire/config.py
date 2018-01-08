import sys
import os
from os.path import join
import json

def getDropboxPath():
    # Gets the Dropbox path depending on the platform
    fin = None
    if sys.platform == 'linux':
        fin = open(join(os.getenv('HOME'), '.dropbox/info.json'))
    if sys.platform == 'win32' or sys.platform == 'cygwin':
        fin = open(join(os.getenv('LOCALAPPDATA'), 'Dropbox\info.json'))
    else: # sys.platform == 'linux':
        fin = open(join(os.getenv('HOME'), '.dropbox/info.json'))
        
    jsn = json.load(fin)
    fin.close()

    return jsn['personal']['path']

_DROPBOX_PATH = getDropboxPath()
_IMAGES_TMP = join(_DROPBOX_PATH, 'Frigidaire')
_FRIGIDAIRE_IMAGES = join(_DROPBOX_PATH, 'Marketplace Images', 'Appliance Images')

