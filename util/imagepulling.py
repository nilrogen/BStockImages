"""
" This file contains functions to search a website.
" I'll probably add more functionality later. 
"
"
" Author: Michael Gorlin
" Date: 2018-03-29
"""

import manifestparser as mp

def search_site(searchurl, parser):
    HEADER = { 'User-Agent' : 'Mozilla/5.0' }

    with rq.get(search, headers=HEADER) as req:
        print(req.status_code)
        if req.status_code == 200:
            parser.feed(req.text)
