"""
" @author Michael Gorlin
" @date 2018-01-17
"
" This file contains the class definitions that represent the elements in 
" each table.
"""
class dbProperty(object):
    """
    " This class serves as to contain information regarding the changes
    " of an element in the table. Most importantly it saves whether the
    " data has changed since its creation. It also enforces type and
    " has stores a default value. If pk is true than changes to the value
    " are not marked. 
    """
    def __init__(self, default, ptype, changed = False, pk=False):
        if default is not None and type(default) is not ptype:
            raise ValueError("Default does not match type provided")
        self._value = default
        self._default = default
        self._changed = changed
        self._ptype = ptype
        self._pk = pk

    @property
    def primarykey(self):
        return self._pk

    @property
    def value(self):
        return self._value
    @value.setter
    def value(self, val):
        if val is not None and type(val) is not self._ptype:
            raise ValueError('Value does not match type')
        if self._value is val:
            return
        self._value = val
        self._changed = not self._pk
        if self._pk:
            self._default = self._value

    @property
    def changed(self):
        return self._changed

    @property
    def ptype(self):
        return self._ptype

    @property
    def default(self):
        return self._default
    @default.setter
    def default(self, val):
        if val is not None and type(val) is not self._ptype:
            raise ValueError('Default does not match type')
        self._default = val
        
    def reset(self):
        self._value = self._default
        self._changed = False

    def __str__(self):
        return '{} {}'.format(self.value, self.changed)

class DBObject(object):
    """
    " Base class for each Table representation
    " Assumes correct structure for subclasses:
    " Class variables should be of type dbProperty, and they should
    " be named exactly as they are in the Column names in the Table. 
    "
    " Class variables should also not be accessed directly and should
    " only be accessed using the getValue, getSQLValue, setValue,  methods. 
    """
    def __str__(self):
        s = ''
        for key in self.__dict__:
            s+= '{} {}\n'.format(key, self.__dict__[key])
        return s

    def getValue(self, key):
        return self.__dict__[key].value

    def getSQLValue(self, key):
        """
        " This function returns a valid sql representation of the object.
        " Converting: None => NULL
        " Quoting strings and correctly formating quotes. 
        " Representing other types as their string definition. 
        """
        v = self.__dict__[key]
        if v.value is None:
            return "NULL"
        if v.ptype == str:
            return "\"%s\"" % v.value.replace('\"', '\\"')
        return str(v.value)

    def setValue(self, key, value):
        self.__dict__[key].value = value
    
    def valueChanged(self, key):
        return self.__dict__[key].changed

    def addTo(self, other):
        if type(self) is not type(other):
            raise ValueError("Types do not match")
        for k in self.__dict__: 
            v1, v2 = self.__dict__[k], other.__dict__[k]
            if v1.value is None and v2.value is not None:
                v1.value = v2.value
        return self

class Item(DBObject):
    def __init__(self):
        self.ModelNumber        = dbProperty(None, str, pk=True)
        self.bstockCategory     = dbProperty(None, str)
        self.bstockSubcategory  = dbProperty(None, str)
        self.Brand              = dbProperty(None, str)
        self.MSRP               = dbProperty(None, float)
        self.MAP                = dbProperty(None, float)
        self.Weight             = dbProperty(None, float)
        self.ShipWeight         = dbProperty(None, float)
        self.ImageLocation      = dbProperty(None, str)
        self.ImageMime          = dbProperty(None, str)
    
    @staticmethod
    def load_values(valdict):
        item = Item()
        for key in valdict:
            if key in item.__dict__:
                prop = item.__dict__[key]
                if valdict[key] is not None:
                    prop.default = prop.ptype(valdict[key])
                    prop.reset()
        return item

class ItemDescription(DBObject):
    def __init__(self):
        self.ModelNumber    = dbProperty(None, str, pk=True)
        self.idMarketplace  = dbProperty(None, int, pk=True)
        self.SKU            = dbProperty(None, str)
        self.UPC            = dbProperty(None, int)
        self.Description    = dbProperty(None, str)
        self.RetailPrice    = dbProperty(None, float)
        self.mktCategory    = dbProperty(None, str)
        self.mktSubcategory = dbProperty(None, str)

    @staticmethod
    def load_values(valdict):
        item = ItemDescription()
        for key in valdict:
            if key in item.__dict__:
                prop = item.__dict__[key]
                if valdict[key] is not None:
                    prop.default = prop.ptype(valdict[key])
                    prop.reset()
        return item
