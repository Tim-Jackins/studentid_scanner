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
	ramp_frames = 5 #This decides how much ramp the camera has to prepare
	# Ramp the camera - these frames will be discarded and are only used to allow webcam to adjust light levels, if necessary
	for i in range(ramp_frames):
		temp = get_image(camera)
	print('Taking image...')
	camera_capture = get_image(camera)
	img = cv2.cvtColor(camera_capture, cv2.COLOR_BGR2GRAY)
	im_pil = Image.fromarray(img)
	return im_pil

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--transition", required=False, default='y', help='The transition state of the student y for entering else n')
args = vars(ap.parse_args())

# Arguments
dir_path = '.'
transition = 'Entering' if args['transition'] == 'y' else 'Exiting'


print('Changing settings') #THIS IS BUT A TEMPORARY FIX
try:
	webcam_settings = { 'focus_auto' : 0, 'focus_absolute' : 255 }
	for setting in webcam_settings:
		out = os.popen('v4l2-ctl -d /dev/video1 -c {0}={1}'.format(setting, str(webcam_settings[setting])))
		#print('The out length is: {0}'.format(len(str(out.read()))))
		if not len(str(out.read())) == 0:
			raise ValueError('Driver error with webcam')
except Exception as e:
	print('Retrying\n\n')
	print('Taking throw away photo...')
	camera_port = 1
	camera = cv2.VideoCapture(camera_port)
	camera.set(3, 1280) # set the resolution
	camera.set(4, 720)
	card = take_image(camera)
	card = take_image(camera)
	camera.release()
	del(camera)
	subprocess.call(['python3', 'scan_and_write.py', '-t', transition])

print('Taking photo...')
camera_port = 1
camera = cv2.VideoCapture(camera_port)
camera.set(3, 1280) # set the resolution
camera.set(4, 720)
card = take_image(camera)
card = take_image(camera)

print('Processing photo...')
card = card.crop((0,560,1100,645))
card.convert('L')
enhancer = ImageEnhance.Contrast(card)
card = enhancer.enhance(1)
card.save('name.jpg')

print('Reading photo...')
name = os.popen('gocr -i name.jpg -f ASCII').read()
print(name)
studentid = 'NA'
try:
	info_to_write = []
	info_to_write.append(name)
	info_to_write.append('\n')
	info_to_write.append(studentid)
	info_to_write.append(transition)

	print('Name: {0}{1}Studentid: {2}{1}Transition: {3}'.format(*info_to_write))

	print('Writing to spreadsheet')
	subprocess.call(['python3', 'write_to_sheet.py', '-n', name, '-i', studentid, '-t', transition])
except Exception as e:
	print('Printing exception... {0}'.format(e))
	print(cardText)
	print('Retrying\n\n')
	card.save('card_fail.jpg')
	camera.release()
	del(camera)
	subprocess.call(['python3', 'scan_and_write.py', '-t', transition])
	
	#print('Writing error to spreadsheet')
	#subprocess.call(['python3', 'write_to_sheet.py', '-e', 1, '-em', cardText, '-ex', e])'''