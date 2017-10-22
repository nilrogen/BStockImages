from tkinter import *
import pyperclip as pc

from random import shuffle

import countfiles as cf

class ItemListIterator:
    def __init__(self, itemlist):
        self.iterator = iter(itemlist)
        self.current = next(self.iterator)

    def getValue(self):
        return self.current

    def next(self):
        self.current = next(self.iterator)

def btn_found_fn(itemiter, tbox_text, lbl_text):
    btn_next_fn(itemiter, tbox_text)
    lbl_text.set(int(lbl_text.get()) + 1)

def btn_next_fn(itemiter, tbox_text):
    itemiter.next()
    tbox_text.set(itemiter.getValue().query())
    pc.copy(tbox_text.get())
    

if __name__ == '__main__':
    itemlist = list(cf.generateSet())
    shuffle(itemlist)
    itemiter = ItemListIterator(itemlist)

    root = Tk()
    root.minsize(500, 200)

    rframe = Frame(root)
    rframe.grid(row=0, sticky=N+S+E+W)
    #rframe.pack(fill=BOTH, expand=True)

    tbox_text = StringVar()
    tbox_text.set(itemiter.getValue().query())
    tbox = Entry(rframe, textvariable=tbox_text)
    tbox.grid(row = 0, columnspan=3, sticky=W+E)

    btn_cpy = Button(rframe, text='Copy Text', command=lambda: pc.copy(tbox_text.get()))
    btn_cpy.grid(row = 1, column = 0, sticky=W+E)

    btn_cpy_inum = Button(rframe, text='Copy Item Number', \
                            command= lambda: pc.copy(str(itemiter.getValue().itemnum)))
    btn_cpy_inum.grid(row = 1, column = 1, sticky=E+W)

    lbl_text = StringVar()
    lbl_text.set('0')
    lbl_items = Label(rframe, textvariable=lbl_text)
    lbl_items.grid(row=1, column=2, sticky=E+W)

    btn_found = Button(rframe, text='Found', \
                        command=lambda: btn_found_fn(itemiter, tbox_text, lbl_text))
    btn_found.grid(row = 2, column = 0, sticky=W+E)

    btn_next = Button(rframe, text='Next', \
                        command=lambda: btn_next_fn(itemiter, tbox_text))
    btn_next.grid(row = 2, column = 1, sticky=W+E)

    btn_quit = Button(rframe, text='Quit')
    btn_quit.grid(row = 2, column = 2, sticky=E+W)

    root.minsize(250, 100)

    root.mainloop()
    



        

