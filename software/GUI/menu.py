#!/usr/bin/python3
import subprocess
from tkinter import *
import math

class testing:
	def write_byte(self, byte):
		self.e.insert(END, byte)
	def clear_all(self):
		self.e.delete(0,END)
	def convert(self):
		self.value = int(str(self.e.get()), 2)
		self.e.delete(0,END)
		self.e.insert(0, self.value)
	def __init__(self, root):
		root.title('Testing') 
		root.geometry()
		self.e = Entry(root)
		self.e.grid(row=0,column=0,columnspan=2,pady=4)
		self.e.focus_set() #Sets focus on the input text area
		#Generating Buttons
		Button(root,text='0', width=10 ,command=lambda:self.write_byte('0')).grid(row=1, column=0)
		Button(root,text='1', width=10, command=lambda:self.write_byte('1')).grid(row=1, column=1)
		Button(root,text='clear', width=10, command=lambda:self.clear_all()).grid(row=2, column=0)
		Button(root,text='convert', width=10, command=lambda:self.convert()).grid(row=2, column=1)
		#Button(root,text="translate",width=10,command=  ).grid(row=1, column=0, columnspan=2)

class studentid_scanner:
	def scan_card():
		subprocess.call(['python3', '../commands/scan_and_write.py'])
	def __init__(self, root):
		root.title('Student ID Reader') 
		root.geometry()
		self.e = Entry(root)
		self.e.grid(row=0,column=0, columnspan=2, pady=1)
		self.e.focus_set() #Sets focus on the input text area
		#Generating Buttons
		Button(root,text="Scan a new card", width=10, command = lambda:self.scan_card).grid(row=0, column=0, columnspan=2)

if __name__ == '__main__':
	root = Tk()
	obj = testing(root)
	#obj = studentid_scanner(root)
	root.mainloop()