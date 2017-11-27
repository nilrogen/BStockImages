from tkinter import *
from PIL import Image, ImageTk

import pyperclip as pc
import bingimage as bi

from config import *
from random import shuffle

import procman as pm
from fuzzywuzzy import fuzz

class ItemListIterator:
    def __init__(self, itemlist):
        self.iterator = iter(itemlist)
        self.current = next(self.iterator)

    def getValue(self):
        return self.current

    def next(self):
        self.current = next(self.iterator)

def btn_found_fn(itemiter):
    btn_next_fn(itemiter)
    lbl_text = stringvars['lbl_text']
    lbl_text.set(int(lbl_text.get()) + 1)

def btn_next_fn(itemiter):
    itemiter.next()
    tbox_text = stringvars['tbox_text']
    tbox_text.set(itemiter.getValue().query())
    pc.copy(tbox_text.get())

def main_frame(root, itemiter):
    global stringvars
    rframe = Frame(root)
    #rframe.pack(fill=BOTH, expand=True)

    stringvars['tbox_text'] = StringVar()
    tbox_text = stringvars['tbox_text']
    tbox_text.set(itemiter.getValue().query())
    tbox = Entry(rframe, textvariable=tbox_text, width=40)
    tbox.grid(row = 0, columnspan=3, sticky=W+E)

    btn_cpy = Button(rframe, text='Copy Text', command=lambda: pc.copy(tbox_text.get()))
    btn_cpy.grid(row = 1, column = 0, sticky=W+E)

    btn_cpy_inum = Button(rframe, text='Copy Item Number', \
                            command= lambda: pc.copy(str(itemiter.getValue().itemnum)))
    btn_cpy_inum.grid(row = 1, column = 1, sticky=E+W)

    stringvars['lbl_text'] = StringVar()
    lbl_text = stringvars['lbl_text']
    lbl_text.set('0')
    lbl_items = Label(rframe, textvariable=lbl_text)
    lbl_items.grid(row=1, column=2, sticky=E+W)

    btn_found = Button(rframe, text='Found', \
                        command=lambda: btn_found_fn(itemiter))
    btn_found.grid(row = 2, column = 0, sticky=W+E)

    btn_next = Button(rframe, text='Next', \
                        command=lambda: btn_next_fn(itemiter))
    btn_next.grid(row = 2, column = 1, sticky=W+E)

    btn_quit = Button(rframe, text='Quit')
    btn_quit.grid(row = 2, column = 2, sticky=E+W)

    rframe.grid(row=0,column=0,sticky=N+W)
    
def get_next_picture(lbl_image, searchiter):
    search = bi.bingValueResult(next(searchiter))
    img = search.downloadImage()
    img = img.resize((300, 300))
    pho_current = ImageTk.PhotoImage(img)

    lbl_image.config(image = pho_current)
    lbl_image.photo = pho_current
    lbl_image.update()

    set_values(search)
    generate_ratio_values(search)

def set_values(result):
    global stringvars

    stringvars['host'].set(str(result.hostLocation()))
    stringvars['name'].set(str(result.name()))
    stringvars['link'].set(str(result.contentLink()))

def generate_ratio_values(result):
    global stringvars
    itm = itemiter.getValue()
    name = stringvars['name'].get()


    stringvars['ratios'].set('({}, {}, {})'.format( \
                fuzz.UQRatio(itm.description, name), \
                fuzz.UWRatio(itm.description, name), \
                fuzz.partial_ratio(itm.description, name)))
                    
    
def picture_frame(root):
    global stringvars, itemiter
    pframe = Frame(root)
    searchRes = None
    while True:
        searchRes = bi.imageSearch(itemiter.getValue().query())
        if searchRes.valueCount() != 0:
            break
        itemiter.next()
        
    searchiter = iter(searchRes.values())
    search = bi.bingValueResult(next(searchiter))
    img = search.downloadImage()
    img = img.resize((300, 300))
    pho_current = ImageTk.PhotoImage(img)
    
    lbl_image = Label(pframe, image=pho_current)
    lbl_image.photo = pho_current
    lbl_image.grid(row=0, column=0, rowspan=2, columnspan=2,sticky=N+S+E+W)

    btn_save = Button(pframe, text='Save')
    btn_save.grid(row=3, column=0, sticky=E+W)

    btn_next = Button(pframe, text='Next', command=\
        lambda: get_next_picture(lbl_image,searchiter))
    btn_next.grid(row=3, column=1, sticky=E+W)

    iframe = Frame(root, bd=2, relief=SUNKEN)

    stringvars['host'] = StringVar("")
    stringvars['name'] = StringVar("")
    stringvars['link'] = StringVar("")
    stringvars['ratios'] = StringVar("")

    generate_ratio_values(search)
    set_values(search)
    tbox_name_text = stringvars['name']
    tbox_name = Entry(iframe, textvariable=tbox_name_text, width=40)
    tbox_name.grid(row=0, column=0, sticky=N+W+E)

    tbox_host_text = stringvars['host']
    tbox_host = Entry(iframe, textvariable=tbox_host_text, width=40)
    tbox_host.grid(row=1, column=0, sticky=N+W+E)

    tbox_link_text = stringvars['link']
    tbox_link = Entry(iframe, textvariable=tbox_link_text, width=40)
    tbox_link.grid(row=2, column=0, sticky=N+E+W)

    tbox_ratio_text = stringvars['ratios']
    tbox_ratio = Entry(iframe, textvariable=tbox_ratio_text, width=40)
    tbox_ratio.grid(row=3, column=0, sticky=N+E+W)

    pframe.grid(row=0, column=1, rowspan=2, sticky=N+W+E+S)
    iframe.grid(row=1, column=0, sticky=N+E+S+W)
    

if __name__ == '__main__':
    global stringvars, itemiter
    itemlist = list(pm.getMissing())
    shuffle(itemlist)
    itemiter = ItemListIterator(itemlist)

    stringvars = {}

    root = Tk()
    #root.minsize(500, 200)

    #picture_frame(root)
    main_frame(root, itemiter)



    root.mainloop()
