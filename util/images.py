import requests

import PIL as pil
import PIL.Image as image


_HEADERS = {
    'User-agent' : 'Mozilla/5.0' 
}


def getExt(location):
    mime = location.split('.')[-1]
    return mime

def download_image(location, path):
    ext = getExt(location)

    try: 
        with requests.get(location, stream=True, headers=_HEADERS) as req:
            if req.status_code != 200:
                print('Issue downloading %s' % (location))

            req.raw_decode_content = True
            img = Image.open(req.raw)

            with open(path, 'wb') as fout:
                img.save(fout)
    except OSError as e: 
        print(e)
    except Exception as e:
        print(e)
