import pytesseract
import argparse
import subprocess
import os
import re
import cv2
from PIL import Image, ImageEnhance, ImageFilter

def get_image(camera):
	ramp_frames = 30 #This decides how much ramp the camera has to prepare
	# Ramp the camera - these frames will be discarded and are only used to allow webcam to adjust light levels, if necessary
	print('Ramping camera...')
	for i in range(ramp_frames):
		temp = get_image(camera)
	print('Taking image...')
	camera_capture = get_image(camera)
	del(camera)
	img = cv2.cvtColor(camera_capture, cv2.COLOR_BGR2RGB)
	im_pil = Image.fromarray(img)
	return im_pil

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--transition", required=True, default='y', help='The transition state of the student y for entering else n')
args = vars(ap.parse_args())

# Arguments
dir_path = '.'
transition = 'Entering' if args['transition'] == 'y' else 'Exiting'

#picname = '{0}.jpg'.format(studentname)

print('Scanning photo id...')
#subprocess.call(['convert', picname, '-rotate', '270', picname]) #only rotate if you have to

camera_port = 1
camera = cv2.VideoCapture(camera_port)
card = get_image(camera)

print('Processing photo...')
card = card.filter(ImageFilter.MedianFilter())
enhancer = ImageEnhance.Contrast(card)
card = enhancer.enhance(2)
card = card.convert('1')

#name = card.crop((135, 940, 880, 1020))
#studentid = card.crop((130, 1090, 590, 1150))

card.save('cardadjust.jpg')
subprocess.call(['mogrify', '-format', 'png', 'cardadjust.jpg'])
os.system('rm *.jpg')
os.system('mv cardadjust.png cut_up_card')
os.chdir('cut_up_card')

print('Reading photo...')
cardText = str(pytesseract.image_to_string(Image.open('cardadjust.png')).encode('utf-8'))
try:
	index = cardText.index('b\'') + 2
	while cardText[index].isalpha() or cardText[index] == ' ': index += 1

	print('Name: {0}{1}Studentid: {2}{1}Transition: {3}'.format(
		cardText[cardText.index('b\'') + 2: index], 
		'\n', 
		str(re.findall(r'\D(\d{9})\D', cardText)[0]),
		transition))
	name = cardText[cardText.index('b\'') + 2: index]
	studentid = str(re.findall(r'\D(\d{9})\D', cardText)[0])

	os.chdir('..')
	print('Writing to spreadsheet')
	subprocess.call(['python3', 'write_to_sheet.py', '-n', name, '-i', studentid, '-t', transition])
except Exception as e:
	print('Writing error to spreadsheet')
	subprocess.call(['python3', 'write_to_sheet.py', '-e', 'True', '-em', cardText, '-ex', e])