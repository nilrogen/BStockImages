from tkinter import *
from PIL import Image, ImageTk

import bingimage as bi


from config import *
from random import shuffle

import procman as pm
from fuzzywuzzy import fuzz


class info_frame(frame):
    def __init__(self, root, searchresult):
        super(frame, root, relief=SUNKEN)
        self.searchresult = searchresult


        img = search.downloadImage()
        img = img.resize((200, 200))
        self.photo = ImageTk.PhotoImage(img)

        self.lbl_img = Label(self, image=self.photo)
        self.lbl_img.pack()
    
    def update(self):
        super(frame, self)

    



if __name__ == '__main__':
    root = Tk()

    i = info_frame(
    
    
