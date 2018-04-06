import cv2

def run_preview():
	cv2.namedWindow("preview")
	camera = cv2.VideoCapture(camera_port)
	if camera.isOpened(): # try to get the first frame
		rval, frame = camera.read()
	else:
		rval = False
	while rval:
		cv2.imshow("preview", frame)
		rval, frame = camera.read()
		key = cv2.waitKey(20)
		if key == 27: # exit on ESC
			break
	cv2.destroyWindow("preview")
 
# Captures a single image from the camera and returns it in PIL format
def get_image(camera):
	# read is the easiest way to get a full image out of a VideoCapture object.
	retval, im = camera.read()
	del(camera)
	return im

def take_image(camera, filename):
	camera_capture = get_image(camera)
	file = './' + filename
	cv2.imwrite(file, camera_capture)
	del(camera)

def take_good_image(camera, filename):
	ramp_frames = 30
	# Ramp the camera - these frames will be discarded and are only used to allow v4l2
	# to adjust light levels, if necessary
	for i in range(ramp_frames):
		temp = get_image(camera)
	print("Taking image...")
	# Take the actual image we want to keep
	camera_capture = get_image(camera)
	file = './' + filename
	# A nice feature of the imwrite method is that it will automatically choose the
	# correct format based on the file extension you provide. Convenient!
	cv2.imwrite(file, camera_capture) 
	# You'll want to release the camera, otherwise you won't be able to create a new
	# capture object until your script exits
	del(camera)

if __name__ == '__main__':
	camera_port = 1
	camera = cv2.VideoCapture(camera_port)
	take_image(camera, 'test_img_bad.png')
	take_good_image(camera, 'test_img_good.png')