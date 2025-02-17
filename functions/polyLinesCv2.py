# Python program to explain 
# cv2.polylines() method 

import cv2
import numpy as np

# path
path = r"C:\Users\gustavonc\Pictures\SGCAM_20241016_182624134.jpg"

# Reading an image in default
# mode
image = cv2.imread(path)

# Window name in which image is
# displayed
window_name = 'Image'

# Polygon corner points coordinates
pts = np.array([[25, 70], [25, 160], 
				[110, 200], [200, 160], 
				[200, 70], [110, 20]],
			np.int32)

pts = pts.reshape((-1, 1, 2))

isClosed = True

# Blue color in BGR
color = (255, 0, 0)

# Line thickness of 2 px
thickness = 2

# Using cv2.polylines() method
# Draw a Blue polygon with 
# thickness of 1 px
image = cv2.polylines(image, [pts], 
					isClosed, color, thickness)

# Displaying the image
while(1):
	
	cv2.imshow('image', image)
	if cv2.waitKey(20) & 0xFF == 27:
		break
		
cv2.destroyAllWindows()
