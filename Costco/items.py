
class Item(object):
    def __init__(self, itemnum, description, found=False, category=None, imagename='', searched=False):
        self.itemnum = int(itemnum)
        self.description = description
        self.category = category
        self.extretail = -1.0
        self.found = found
        self.imagename = imagename
        self.searched = False

    def __hash__(self):
        return hash(self.itemnum)

    def __eq__(self, other):
        return hash(self) == hash(other)
    def __lt__(self, other):
        return self.itemnum < other.itemnum
    def __le__(self, other):
        return self.itemnum <= other.itemnum
    def __gt__(self, other):
        return self.itemnum > other.itemnum
    def __ge__(self, other):
        return self.itemnum >= other.itemnum
    def __cmp__(self, other):
        return self.itemnum - other.itemnum

    def __str__(self):
        if self.extretail == -1:
            return "{} {} {}".format(self.itemnum, self.description, \
                                     self.found)
        return "{} {} {}".format(self.itemnum, self.description, \
                                 self.extretail)
    def __repr__(self):
        return "{} {} {}".format(self.itemnum, self.description, self.found)

    def query(self):
        return "costco {} {}".format(self.itemnum, self.description)

    @staticmethod
    def toJSON(item):
        retv = { 'item-num' : item.itemnum, \
                 'description' : item.description, \
                 'found' : item.found, \
                 'image-name' : item.imagename, \
                 'searched' : item.searched }
        if item.extretail != -1:
            retv['ext-retail'] = item.extretail
        if item.category != None:
            retv['category'] = item.category
        return retv


    @staticmethod
    def fromJSON(jsn):
        try:
            itn = jsn['item-num']
            des = jsn['description']
            found = jsn['found']
            imn = jsn['image-name']
                
            retv = Item(itn, des, found, None, imn)

            if 'searched' in jsn.keys():
                retv.searched = jsn['searched']
            if 'ext-retail' in jsn.keys():
                retv.extretail = jsn['ext-retail']
            if 'category' in jsn.keys():
                retv.category = jsn['category']
            return retv
        except:
            raise ValueError('Value is not correctly formatted')
            
