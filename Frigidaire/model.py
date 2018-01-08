import locale 
import json

_JSON_KEYS = {
    'model-number'  : 'model-number',
    'brand'         : 'brand',
    'found'         : 'found',
    'searched'      : 'searched',
    'description'   : 'description',
    'section'       : 'section',
    'category'      : 'category',
    'msrp'          : 'msrp',
    'ship-weight'   : 'ship-weight',
    'weight'        : 'weight',
    'img-src'       : 'img-src',
    'img-location'  : 'img-location'
}

class Model(object):
    def __init__(self, modelnumber):
        self.modelnumber = modelnumber
        self.found = False
        self.searched = False
        self.brand = 'Frigidaire'
        self.description = ''
        self.category = ''
        self.section = ''
        self.msrp = 0.0

        self.weight = ''
        self.shipweight = ''

        self.imagesrc = ''
        self.imageloc = ''

    def __cmp__(self, other):
        return cmp(self.modelnumber, other.modelnumber)
    def __lt__(self, other):
        return self.modelnumber < other.modelnumber

    def __str__(self):
        return "{}".format(self.modelnumber)
    def __repr__(self):
        return str(self) 

    def setfromWebData(self, data):
        def fromKey(key):
            if key in data.keys():
                return data[key]
            return ''

        if self.modelnumber != fromKey('Product Number'):
            raise ValueError('Model Numbers do not match {} vs {}'.format(modelnumber, fromKey('Product Number')))

        self.searched = True
        self.description = fromKey('Product Name')

        self.msrp = float(fromKey('Product Price'))         
        if self.msrp == 0.0: #indicates that the item is discontinued
            return 

        self.section = fromKey('Site Section')
        self.category = fromKey('Page Category')

    @staticmethod
    def fromJSON(json):

        def getKey(key, default):
            if _JSON_KEYS[key] in json.keys():
                return json[_JSON_KEYS[key]]
            return default
        
        modelnumber = getKey('model-number', None)
        if modelnumber == None:
            estr = 'JSON format incorrect: Missing {}'
            raise ValueError(estr.format(_JSON_KEYS['model-number']))

        retv = Model(modelnumber)

        retv.brand = getKey('brand', 'Frigidaire')
        retv.found = getKey('found', False)
        retv.searched = getKey('searched', False)
        retv.description = getKey('description', '')
        retv.section = getKey('section', '')
        retv.category = getKey('category', '')
        retv.msrp = float(getKey('msrp', '0.0'))
        retv.weight = getKey('weight', '')
        retv.shipweight = getKey('ship-weight', '')
        retv.imagesrc = getKey('img-src', '')
    
        return retv

    @staticmethod
    def toJSON(model):
        retv = {}

        def setKey(key, value):
            if value != '':
                retv[_JSON_KEYS[key]] = value

        setKey('model-number',  model.modelnumber) 
        setKey('brand',         model.brand)
        setKey('found',         model.found) 
        setKey('searched',      model.searched) 

        setKey('description',   model.description) 

        if model.msrp != 0.0:
            setKey('msrp', model.msrp)

        setKey('section',       model.section) 
        setKey('category',      model.category) 

        setKey('weight',        model.weight)
        setKey('ship-weight',   model.shipweight)

        setKey('img-src',       model.imagesrc)

        return retv
