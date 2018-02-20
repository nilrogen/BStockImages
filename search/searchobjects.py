"""
Here we want a standard storage object for various elements found in each 
marketplace's manifests. Namely: Marketplace Name, Item or Model number,
Brand, and Description.

@author Michael Gorlin
@date 2018-02-13
"""

from pprint import *

class SearchItem(object):
    def __init__(self):
        self.marketplace = None
        self.itemnumber  = None
        self.brand       = None
        self.description = None

        self.reason = None
        self.searchresult = None

    def getQuery(self, options):
        """
        This function generates an appropriate query given an "options" string.
        The options String is comprised of characters that represent elements
        in the class:
            'M' : Marketplace
            'I' : Item Number
            'B' : Brand
            'D' : Description

        Example Queries would be:
            'ID'  => <Item Number> <Description>
            'MBD' => <Marketplace> <Brand> <Description>
        """
        retv = ''
        for c in options.upper():
            if c == 'M': 
                retv += str(self.marketplace)
            elif c == 'I':
                retv += str(self.itemnumber)
            elif c == 'B':
                retv += str(self.brand)
            elif c == 'D':
                retv += str(self.description)
            retv += ' '
        return retv[:-1]

class SearchReason(object):
    """
    This class holds the reasons success or failure in the search.
    """
    def __init__(self, success, **kwargs):
        self.reasons = {}
        self.reasons['success'] = success
        for k in kwargs:
            self.reasons[k] = kwargs[k]

    def __getattr__(self, name):
        if name != 'reasons' and name in self.reasons:
            return self.reasons[name]
        return getattr(self, name)

    def __setattr__(self, name, value):
        if name != 'reasons':
            self.reasons[name] = value
        super(SearchReason, self).__setattr__(name, value)

    def toJSON(self):
        return self.reasons

if __name__ == '__main__':
    reason = SearchReason(False)

    reason.timestamp = '2018-02-15'
    reason.pictureurl = 'www.website.com/fakeimg.jpg'
    reason.confidence = 50

    pprint(reason.toJSON())
