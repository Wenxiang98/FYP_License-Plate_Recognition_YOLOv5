from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from tkinter import messagebox
import tkinter
import os
import sys
import time

path= 0 

def build():
    root = Tk()
    root.geometry("900x600")
    root.maxsize(width = 1080, height = 1200)
    root.resizable(width=True, height=True)
    root.title('License Plate Recognition System')
    return root

def openfn():
    filename = filedialog.askopenfilename(title='open')
    global path
    path = filename
    return filename

def open_img():
    x = openfn()
    show(x)

def show(x):
    img = Image.open(x)
    img = img.resize((852, 480), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel = Label(root, image=img)
    panel.image = img
    panel.place(x = 10, y = 50)

    f=open("path.txt", "w")
    f.write(x)

 

def helloCallBack():
    carplate=""
    path_txt = open("path.txt", "r")
    path_txt = path_txt.read()
    cmd='python detect.py --source '+ str(path_txt) +' --weights ./model1.pt --conf 0.25'
    os.system(cmd)
    time.sleep(3)
    # space="                                                                         "
    # msg = tkinter.Message(root, text = space, width = 1000)
    file_path='LP.txt'
    # check if size of file is 0
    if os.stat(file_path).st_size == 0:
        print('No License Plate Detected.')
        data = "No License Plate Detected.                                     "
        msg = tkinter.Message(root, text = data, width = 2000)
        msg.place(x=350,y=550 )
    else:
        f = open('LP.txt',"r")
        carplate = f.read()
        data = "License Plate Number is " + str(carplate) + "                             "
        msg = tkinter.Message(root, text = data, width = 2000)
        msg.place(x=350,y=550 )


root = build()
btn = Button(root, text='Open image', command=open_img).pack()
B=tkinter.Button(root,text="Recognize License Plate",command= helloCallBack)
B.pack()


root.mainloop()
