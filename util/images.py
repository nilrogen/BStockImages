import requests

import PIL as pil
import PIL.Image as Image

_HEADERS = {
    'User-Agent' : 'Mozilla/5.0' 
}

def download_image(url):
    try: 
        with requests.get(url, stream=True, headers=_HEADERS) as req:
            if req.status_code != 200:
                print('Issue downloading %s' % (location))

            req.raw_decode_content = True
            img = Image.open(req.raw)
            return img
    except OSError as e: 
        print(e)
    except Exception as e:
        print(e)

    return None
