import pytesseract
import argparse
import subprocess
import os
import re
import cv2
import time
from PIL import Image, ImageEnhance, ImageFilter

def get_image(camera):
	# read is the easiest way to get a full image out of a VideoCapture object.
	retval, im = camera.read()
	del(camera)
	return im

def take_image(camera):
	#ramp_frames = 1 #This decides how much ramp the camera has to prepare
	# Ramp the camera - these frames will be discarded and are only used to allow webcam to adjust light levels, if necessary
	#print('Ramping camera...')
	#for i in range(ramp_frames):
	#	temp = get_image(camera)
	print('Taking image...')
	camera_capture = get_image(camera)
	del(camera)
	img = cv2.cvtColor(camera_capture, cv2.COLOR_BGR2RGB)
	im_pil = Image.fromarray(img)
	return im_pil

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--transition", required=False, default='y', help='The transition state of the student y for entering else n')
args = vars(ap.parse_args())

# Arguments
dir_path = '.'
transition = 'Entering' if args['transition'] == 'y' else 'Exiting'

#picname = '{0}.jpg'.format(studentname)

print('Scanning photo id...')
#subprocess.call(['convert', picname, '-rotate', '270', picname]) #only rotate if you have to

#os.system('./set_setting.sh')
#out = os.popen('v4l2-ctl -d /dev/video1 --list-ctrls').read()
#print(out)
#search_str = 'focus_auto (bool)   : default=1 value='
#if bool(int(out[out.index(search_str) + len(search_str):out.index(search_str) + len(search_str) + 1])):
#	print('Changing settings')
#	webcam_settings = { 'focus_auto' : 0, 'focus_absolute' : 255 }
#	for setting in webcam_settings:
#		subprocess.call(['v4l2-ctl -d 1 --set-ctrl {0}={1}'.format(setting, str(webcam_settings[setting]))], shell=True)
#else:
#	print('Setting focus')
#	subprocess.call(['v4l2-ctl -d 1 --set-ctrl {0}={1}'.format('focus_absolute', '255')], shell=True)

print('Changing settings')
webcam_settings = { 'focus_auto' : 0, 'focus_absolute' : 255 }
for setting in webcam_settings:
	subprocess.call(['v4l2-ctl -d 1 --set-ctrl {0}={1}'.format(setting, str(webcam_settings[setting]))], shell=True)

camera_port = 1

camera = cv2.VideoCapture(camera_port)
camera.set(3, 1280) # set the resolution
camera.set(4, 720)

card = take_image(camera)

camera.release

print('Processing photo...')
card = card.filter(ImageFilter.MedianFilter())
#enhancer = ImageEnhance.Contrast(card)
#card = enhancer.enhance(2)
card = card.convert('L')
card = card.crop((500, 480, 1185, 700))

card.save('cardadjust.jpg')
#subprocess.call(['mogrify', '-format', 'png', 'cardadjust.jpg'])
#os.system('rm *.jpg')
#os.system('mv cardadjust.png cut_up_card')
#os.chdir('cut_up_card')

print('Reading photo...')
cardText = str(pytesseract.image_to_string(card).encode('utf-8'))
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

	print('Writing to spreadsheet')
	subprocess.call(['python3', 'write_to_sheet.py', '-n', name, '-i', studentid, '-t', transition])
except Exception as e:
	print('Print exception: {0}'.format(e))
	print('Writing error to spreadsheet')
	subprocess.call(['python3', 'write_to_sheet.py', '-e', 1, '-em', cardText, '-ex', e])