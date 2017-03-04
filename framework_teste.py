#!/usr/bin/env python

from Tkinter import *

class Application(Frame):
    def say_hi(self):
        print "hi there, everyone!"

    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        self.QUIT.pack({"side": "bottom"})

        self.hi_there = Button(self)
        self.hi_there["text"] = "Hello",
        self.hi_there["command"] = self.say_hi

        self.hi_there.pack({"side": "left"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()

# import Tkinter
# import tkMessageBox
#
# top = Tkinter.Tk()
#
# def helloCallBack():
#    tkMessageBox.showinfo( "Hello Python", "Hello World")
#
# B = Tkinter.Button(top, text ="Hello", command = helloCallBack)
#
# B.pack()
# top.mainloop()

# import Tkinter
# import tkMessageBox
#
# top = Tkinter.Tk()
#
# C = Tkinter.Canvas(top, bg="blue", height=250, width=300)
#
# coord = 10, 50, 240, 210
# arc = C.create_arc(coord, start=0, extent=359, fill="red")
#
# C.pack()
# top.mainloop()