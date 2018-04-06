#!/usr/bin/python3
import subprocess
from tkinter import *
import math

root = Tk()

root.title('Student ID Reader') 
root.geometry()
e = Entry(root)
e.grid(row=0,column=0,columnspan=3,pady=3)
#e.focus_set() #Sets focus on the input text area
#div='÷'
#newdiv=self.div#self.div.decode('utf-8')
#Generating Buttons
#Button(master,text="=",width=10,command=lambda:self.equals()).grid(row=4, column=4,columnspan=2)

root.mainloop()