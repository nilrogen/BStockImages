from tkinter import *
from PIL import Image, ImageTk

import bingimage as bi


from config import *
from random import shuffle

import procman as pm
from fuzzywuzzy import fuzz

whitelist = [ ('www.costco.com', 1.5), \
              ('www.costcobusinessdelivery.com', 1.4), \
              ('www.costco.co.uk', 1.4), \
              ('www.costco.ca', 1.4), \
              ('www.amazon.com', 1.25), \
              ('amazon.com', 1.25), \
              ('amazon.co.uk', 1.25), \
              ('www.homedepo.com', 1), \
              ('www.walmart.com', 1), \
              ('www.samsclub.com', 1), \
              ('www.target.com', 1), \
              ('www.kohls.com', 1), \
              ('www.instacart.com', 1), \
              ('www.bjs.com', .9), \
              ('www.walgreens.com', .9), \
              ('www.sears.com', .9), \
              ('www.overstock.com', .9), \
              ('www.lyst.com', .9), \
              ('www.ebay.com', .5) ]

def getPriority(item, value):
    retv = fuzz.UQRatio(item.description, value.name())
    wl = False

    host = value.hostLocation()

    # Loop through whitelist and if host matches multiply return value by priority factor
    for i in range(len(whitelist)):
        if host == whitelist[i][0]:
            retv = round(whitelist[i][1] * retv)
            wl = True
    if retv < 20:
        return -1
    if not wl:  
        return -1
    return retv

class ItemListIterator:
    def __init__(self, itemlist):
        self.iterator = iter(itemlist)
        self.current = next(self.iterator)

    def getValue(self):
        return self.current

    def next(self):
        self.current = next(self.iterator)

class info_frame(Frame):
    def __init__(self, root, searchresult):
        super().__init__(root, relief=SUNKEN, bd=4)
        self.searchresult = searchresult


        img = searchresult.downloadImage()
        img = img.resize((150, 150), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(img)

        self.lbl_img = Label(self, image=self.photo)
        self.lbl_img.grid(row=0, column=0, rowspan=4, columnspan=4, sticky=E+W+S+N)

        self.tbox_host_text = StringVar()
        self.tbox_host_text.set(self.searchresult.hostLocation())
        self.tbox_host = Entry(self, textvariable=self.tbox_host_text)
        self.tbox_host.grid(row=4, column=0, columnspan=4, sticky=E+W)

        self.tbox_name_text = StringVar()
        self.tbox_name_text.set(self.searchresult.name())
        self.tbox_name = Entry(self, textvariable=self.tbox_name_text)
        self.tbox_name.grid(row=5, column=0, columnspan=4, sticky=E+W)

        self.tbox_prio_text = StringVar()
        self.tbox_prio_text.set(str(getPriority(itemiter.getValue(), searchresult)))
        self.tbox_prio = Entry(self, textvariable=self.tbox_prio_text)
        self.tbox_prio.grid(row=6, column=0, columnspan=4, sticky=E+W)


    def update(self):
        super().update()

def getNextSearchResult():
    global itemiter

    searchRes = None
    for i in range(10):
        searchRes = bi.imageSearch(itemiter.getValue().query())
        if searchRes.valueCount() != 0:
            break
        itemiter.next()
    return searchRes

if __name__ == '__main__':
    global itemiter
    itemlist = list(pm.getFound())
    shuffle(itemlist)
    itemiter = ItemListIterator(itemlist)

    searchRes = getNextSearchResult()

    root = Tk()

    tbox_query_text = StringVar()
    tbox_query_text.set(itemiter.getValue().query())
    tbox_query = Entry(root, textvariable=tbox_query_text)
    tbox_query.grid(row=0, column=0, sticky=E+W+S+N)

    pframe = Frame(root)
    for i in range(min(searchRes.valueCount(), 24)):
        j = i // 8
        iframe = info_frame(pframe, searchRes.getValue(i))
        iframe.grid(row=j, column=i%8, sticky=E+W)
    pframe.grid(row=1, column=0)
    
    root.mainloop() 
