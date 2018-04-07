import pytesseract
import argparse
import subprocess
import os
import re
from PIL import Image, ImageEnhance, ImageFilter

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument('-n', '--name', required=True, default='John Doe', help='Name of student you want to document')
ap.add_argument('-t', '--transition', required=True, default='y', help='Are you y or n for entering?')
ap.add_argument('-l', '--location', required=False, default='.', help='Loaction of where you\'re launching from')
args = vars(ap.parse_args())

# Arguments
dir_path = '.'
studentname = args['name']
transition = 'Entering' if args['transition'] == 'y' else 'Exiting'
os.chdir(args['location'])

picname = '{0}.jpg'.format(studentname)

print('Getting photo id...')
#os.system('cp backup/{0} .'.format(picname))
#subprocess.call(['convert', picname, '-rotate', '270', picname]) #only rotate if you have to
card = Image.open('backup/' + picname) # the second one 

print('Processing photo...')
card = card.filter(ImageFilter.MedianFilter())
enhancer = ImageEnhance.Contrast(card)
card = enhancer.enhance(2)
card = card.convert('1')
#name = card.crop((135, 940, 880, 1020))
#studentid = card.crop((130, 1090, 590, 1150))
#card.save('cardadjust.jpg')
#subprocess.call(['mogrify', '-format', 'png', 'cardadjust.jpg'])
#os.system('rm *.jpg')
#os.system('mv cardadjust.png cut_up_card')
#os.chdir('cut_up_card')

print('Reading photo...')
#cardText = str(pytesseract.image_to_string(Image.open('cardadjust.png')).encode('utf-8'))
cardText = str(pytesseract.image_to_string(card).encode('utf-8'))
#try:
index = cardText.index('b\'') + 2
while cardText[index].isalpha() or cardText[index] == ' ': index += 1
name = cardText[cardText.index('b\'') + 2: index]
studentid = str(re.findall(r'\D(\d{9})\D', cardText)[0])
#if input('Want to write to the sheet (y for yes): ') == 'y':
if False:
	os.chdir('..')
	print('Writing to spreadsheet')
	subprocess.call(['python3', 'write_to_sheet.py', '-n', name, '-i', studentid, '-t', transition])
else:
	print('Name:		{0}\n\
ID#:		{1}\n\
Transition:	{2}'.format(name, studentid, transition))