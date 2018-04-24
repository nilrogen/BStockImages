"""
" This file contains functions to search a website.
" I'll probably add more functionality later. 
"
" Author: Michael Gorlin
" Date: 2018-03-29
"""
from html.parser import HTMLParser

import requests as rq

class Content(object):
    def __init__(self, tagname, kattr, kval):
        self.knownkv = (kattr, kval)
        self.tagname = tagname
        self.state = 0
        self.value = None
        self.found = False 

    def find(self, tag, attrs):
        if not self.found:
            if self.tagname == tag and self.knownkv in attrs:
                self.state = 1

    def handleContent(self, data):
        if not self.found and self.state == 1:
            self.value = data
            self.found = True

    def reset(self):
        self.state = 0
        self.value = None
        self.found = False

class InsideContent(Content):
    def __init__(self, tagname, insidetag, kattr, kval):
        super(InsideContent, self).__init__(tagname, kattr, kval)
        self.insidetag = insidetag

    def find(self, tag, attrs):
        if not self.found:
            if self.state == 1:
                if tag == self.insidetag:
                    self.state = 2
                    return
            super(InsideContent, self).find(tag, attrs)

    def handleContent(self, data):
        if self.state == 2 and not self.found:
            self.value = data
            self.found = True
        
class Tag(Content):
    def __init__(self, tagname, kattr, kval, uattr):
        super(Tag, self).__init__(tagname, kattr, kval)
        self.uattr = uattr

    def find(self, tag, attrs):
        if not self.found:
            if self.tagname == tag and self.knownkv in attrs:
                for k, v in attrs:
                    if k == self.uattr:
                        self.value = v
                        self.found = True
                        break


class MarketplaceParser(HTMLParser):
    """
    " This class is passed a mapping of how to parse a html document
    " then parses it. Each value in the mapping is its own state machine. 
    "
    " Needs to handle:
    " 1. When the desired value is an attribute of a tag. Use Tag object.
    " 2. When the disired value is the content of a tag with attributes. 
    "    Use Content object.
    " 3. When the disired value is the content of a tag whose parent has 
    "    desired attributes. Use InsideContent object
    """
    def __init__(self, mapping):
        super(MarketplaceParser, self).__init__()
        self.mapping = mapping
        self.values = dict.fromkeys(mapping, None)
        self.state = 0

    def handle_starttag(self, tag, attrs):
        for key in self.mapping:
            self.mapping[key].find(tag, attrs)
    
    def handle_data(self, data):
        for key in self.mapping:
            self.mapping[key].handleContent(data)

    def feed(self, data):
        self.values = dict.fromkeys(self.mapping, None)
        for k in self.mapping:
            self.values[k] = self.mapping[k].reset()
        super(MarketplaceParser, self).feed(data)
    
    def getValues(self):
        for k in self.mapping:
            self.values[k] = str(self.mapping[k].value).strip()
        return self.values


def search_site(searchurl, parser):
    HEADER = { 'User-Agent' : 'Mozilla/5.0' }

    with rq.get(searchurl, headers=HEADER) as req:
        if req.status_code == 200:
            parser.feed(req.text)
            return req.text
    return ''
