from ultralytics import YOLO

# Load a pretrained YOLO model
model = YOLO("pt/linha_11m.pt")

# Perform object detection on an image
results = model("img/image.png")
#results = model.track("videos/output_video.avi")

# Visualize the results
for result in results:
    #print(result.boxes)  # Print detection boxes
    result.show()  # Display the annotated image
    result.save(filename="result6.png")  # Save annotated image
    
res = type(result.boxes)

print(res)