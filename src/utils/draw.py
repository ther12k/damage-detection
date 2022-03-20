import cv2

def draw_rectangle(image, result, resize=100):
	'''
	Draw bounding box, label and clases detection image
	Args:
		img(numpy.ndarray) : image/frame
		result(list) : [[x_min, y_min, x_max, y_max, classes_name, confidence]]
	return : 
		image(numpy.ndarray)
	'''
	if len(result):
		
		x_min, x_max = result[0][0], result[0][2]
		y_min, y_max = result[0][1], result[0][3]
		classes_name = result[1]
		confidence   = int(result[2]*100)
		color 		 = (86, 71, 255)
		# Draw rectangle
		
		# Add label
		cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, 8)
		
	width   = int(image.shape[1] * resize / 100)
	height  = int(image.shape[0] * resize / 100)
	# resize image
	resized = cv2.resize(image, (width, height), interpolation = cv2.INTER_AREA)
	return resized