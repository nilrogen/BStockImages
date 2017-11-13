import sys
import os
import json

def getDropboxPath():
    fin = None
    if sys.platform == 'linux2':
        fin = open('~/.dropbox/info.json')
    elif sys.platform == 'win32':
        fin = open(os.path.join(os.getenv('LOCALAPPDATA'), 'Dropbox\info.json'))
    
    jsn = json.load(fin)
    fin.close()

    return jsn['personal']['path']

_DROPBOX = getDropboxPath()
_MANIFEST_PATH = os.path.join(_DROPBOX, 'Marketplace Images/Costco Manifest')
_IMAGES_PATH = os.path.join(_DROPBOX, 'Marketplace Images/Costco Images')
_FNAME = os.path.join(_MANIFEST_PATH, 'AllFiles.json')
      

#_SAVE_PATH = '/home/michael/Desktop/Output/'
#_SAVE_PATH = '/cygdrive/c/Users/Mike Work/Desktop'
#_SAVE_PATH = "C:\\Users\\Mike Work\\Desktop"

