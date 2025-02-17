# Python program to write 
# text on video 


import cv2 


cap = cv2.VideoCapture(r'C:\Users\gustavonc\Videos\video_linha\exported.mp4') 

valor = [
    {'quantidade' : '1213'},
    {'quantidade' : '123'},
    {'quantidade' : '123123'},
]




while(True): 
	
	# Capture frames in the video 
	ret, frame = cap.read() 

	# describe the type of font 
	# to be used. 
	font = cv2.FONT_HERSHEY_SIMPLEX
    
	# Use putText() method for 
	# inserting text on video 
	cv2.putText(frame, valor[0]['quantidade'] ,(50, 50), font, 1, (0, 255, 255), 2, cv2.LINE_4) 

	# Display the resulting frame 
	cv2.imshow('video', frame) 

	# creating 'q' as the quit 
	# button for the video 
	if cv2.waitKey(1) & 0xFF == ord('q'): 
		break

# release the cap object 
cap.release() 
# close all windows 
cv2.destroyAllWindows() 
