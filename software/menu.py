#!/usr/bin/python3
import subprocess
from tkinter import *
import math
from PIL import Image, ImageTk
from glob import glob
import natsort
import re
import os

class bin_calc:
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

class studentid_scanner_demo:
	def scan_card(self):
		try:
			scan_out = os.popen('python3 demos/reader/read_card.py -n {0} -t y -l demos/reader/'.format(self.tkvar.get())).read()
			self.name = scan_out[scan_out.index('\t\t') + 2 : scan_out.index(' \n')]
			self.id = str(re.findall(r'\D(\d{9})\D', scan_out)[0])
			self.output_area.delete('1.0',END)
			self.output_area.delete('2.0',END)
			self.output_area.delete('3.0',END)
			self.output_area.insert(END, 'Results\n\
Name:		{0}\n\
ID#:		{1}\n'.format(self.name, self.id))
		except:
			self.output_area.delete('1.0',END)
			self.output_area.delete('2.0',END)
			self.output_area.delete('3.0',END)
			self.output_area.insert(END, 'Results\nERROR')
		
	def scanning(self, var):
		print(var)
	def __init__(self, root):
		root.title('Student ID Reader') 
		root.geometry('550x400')
		
		self.header = Label(root, text="This is the scanner")
		self.header.pack(side = TOP)
		self.scan_button = Button(root, text='Scan', command = lambda:self.scan_card())
		self.scan_button.pack()
		self.close_button = Button(root, text='Close', command=root.quit)
		self.close_button.pack()

		self.tkvar = StringVar(root)
		picNames = []
		for file in natsort.natsorted(glob('demos/reader/backup/*.jpg')):
			picNames.append(file[20:].replace('.jpg', ''))
		choices = set(picNames)
		self.tkvar.set(picNames[0]) # set the default option
		popupMenu = OptionMenu(root, self.tkvar, *choices)
		popupMenu.pack()
		# on change dropdown value
		def change_dropdown(*args):
			print(self.tkvar.get())
			rep_img = Image.open('demos/reader/backup/' + self.tkvar.get() + '.jpg')
			scale_const = .25
			if rep_img.width > rep_img.height:
				diff_const = int(rep_img.width / rep_img.height)
				scalew = scale_const * diff_const
				scaleh = scale_const
			else:
				diff_const = int(rep_img.height / rep_img.width)
				scalew = scale_const
				scaleh = scale_const * diff_const
			rep_img = rep_img.resize((int(rep_img.width * scalew), int(rep_img.height * scaleh)))
			rep_tkimg = ImageTk.PhotoImage(rep_img)

			self.card_pic.configure( image = rep_tkimg)
			self.card_pic.image = rep_tkimg
		# link function to change dropdown
		self.tkvar.trace('w', change_dropdown)
		#tkvar.trace('w', change_dropdown)
		#slice image
		img = Image.open('demos/reader/backup/' + self.tkvar.get() + '.jpg')
		scale_const = .25
		if img.width > img.height:
			diff_const = int(img.width / img.height)
			scalew = scale_const * diff_const
			scaleh = scale_const
		else:
			diff_const = int(img.height / img.width)
			scalew = scale_const
			scaleh = scale_const * diff_const
		img = img.resize((int(img.width * scalew), int(img.height * scaleh)))
		tkimg = ImageTk.PhotoImage(img)
		
		self.card_pic = Label(root, image = tkimg)
		self.card_pic.image = tkimg
		self.card_pic.pack(side = LEFT)

		self.output_area = Text(root, height=3, width=40)
		self.output_area.pack(side = RIGHT)
		self.output_area.insert(END, 'Results')

if __name__ == '__main__':
	root = Tk()
	#obj = testing(root)
	obj = studentid_scanner_demo(root)
	root.mainloop()