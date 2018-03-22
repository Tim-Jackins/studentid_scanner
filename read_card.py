import pytesseract
import argparse
import subprocess
import os
from ascii_art import *
from PIL import Image, ImageEnhance, ImageFilter

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--name", required=True, default='John Doe', help='Name of student you want to document')
ap.add_argument("-t", "--transition", required=True, default='y', help='Are you y or n for entering?')
args = vars(ap.parse_args())

# Arguments
dir_path = '.'
studentname = args['name']
#transition = args['transition']
transition = 'Entering' if args['transition'] == 'y' else 'Exiting'

picname = '{0}.jpg'.format(studentname)

os.system('cp backup/{0} .'.format(picname))
subprocess.call(['convert', picname, '-rotate', '270', picname])
card = Image.open(picname) # the second one 

#headshot = card.crop((160, 70, 715, 800))
#eadshot.save('headshot.jpg')

card = card.filter(ImageFilter.MedianFilter())
enhancer = ImageEnhance.Contrast(card)
card = enhancer.enhance(2)
card = card.convert('1')

#name = card.crop((135, 940, 880, 1020))
#studentid = card.crop((130, 1090, 590, 1150))

card.save('cardadjust.jpg')
#name.save('name.jpg')
#studentid.save('studentid.jpg')

subprocess.call(['mogrify', '-format', 'png', 'cardadjust.jpg'])
#subprocess.call(['mogrify', '-format', 'png', 'headshot.jpg'])
#subprocess.call(['mogrify', '-format', 'png', 'name.jpg'])
#subprocess.call(['mogrify', '-format', 'png', 'studentid.jpg'])
#os.system('rm *.jpg')

os.system('mv cardadjust.png cut_up_card')
	#headshot.png name.png studentid.png cut_up_card')
os.chdir('cut_up_card')
name = pytesseract.image_to_string(Image.open('name.png'))
studentid = pytesseract.image_to_string(Image.open('studentid.png'))

cardText = str(pytesseract.image_to_string(Image.open('cardadjust.png')).encode('utf-8'))

index = cardText.index('b\'') + 2
while cardText[index].isalpha() or cardText[index] == ' ': index += 1

print('Name: {0}{1}studentid: {2}{1}Transition: {3}'.format(
	cardText[cardText.index('b\'') + 2: index], 
	'\n', 
	cardText[cardText.index('ID# ') + 4: cardText.index('ID# ') + 13], 
	transition))

os.chdir('..')
#subprocess.call(['python3', 'write_to_sheet.py', '-n', name, '-i', studentid, 't', transition])