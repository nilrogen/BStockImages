
class Item(object):
    def __init__(self, itemnum, description, found=False, imagename=''):
        self.itemnum = int(itemnum)
        self.description = description
        self.found = found
        self.imagename = imagename
        
    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(self.itemnum)

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
        return "{} {} {}".format(self.itemnum, self.description, self.found)
    def __repr__(self):
        return "{} {} {}".format(self.itemnum, self.description, self.found)

    def query(self):
        return "{} {}".format(self.itemnum, self.description)

    @staticmethod
    def toJSON(item):
        return { 'item-num' : item.itemnum, \
                 'description' : item.description, \
                 'found' : item.found, \
                 'image-name' : item.imagename }

    @staticmethod
    def fromJSON(jsn):
        try:
            itn = jsn['item-num']
            des = jsn['description']
            if not jsn['found']:
                return Item(itn, des)
            imn = jsn['image-name']
            return Item(itn, des, True, imn)
        except:
            raise ValueError('Value is not correctly formatted')
            

class ItemContainer(object):
    def __init__(self):
        self.list = None

    def sort(self):
        pass

    def add(self, item):
        pass
    def remove(self, item):
        pass

    def __in__(self, value):
        return value in self.list
    def __len__(self):
        return len(self.list)
    def __iter__(self):
        pass

class ItemSet(ItemContainer):
    def __init__(self):
        super(ItemSet, self).__init__()
        self.list = set()

    def add(self, item):
        if type(item) is Item and item not in self.list:
            self.list.add(item)
            return True
        return False

    def pop(self):
        return self.list.pop()

    def remove(self, item):
        self.list.remove(item)

    def __iter__(self):
        return ItemListIterator(self.list)

class ItemList(ItemContainer):
    def __init__(self):
        super(ItemList, self).__init__()
        self.list = list()

    def add(self, item):
        if type(item) is Item:
            self.list.append(item)
            return True
        return False

    def remove(self, item):
        if type(item) is Item:
            self.list.remove(item)
            return True
        return False

    def __iter__(self):
        return ItemListIterator(self.list)

class ItemListIterator:
    def __init__(self, itemlist):
        self.iterator = iter(itemlist)
        self.current = next(self.iterator)
        self.previous = None

    def getValue(self):
        return self.current

    def __next__(self):
        return self.next()

    def next(self):
        self.current = next(self.iterator)
        return self.current
        
