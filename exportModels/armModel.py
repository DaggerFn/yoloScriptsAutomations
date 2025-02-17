from ultralytics import YOLO

# Load the exported NCNN model
ncnn_model = YOLO("yolov8n_ncnn_model")

# Run inference
results = ncnn_model("bus.jpg")

for result in results:
    #print(result.boxes)  # Print detection boxes
    result.show()  # Display the annotated image
    result.save(filename="result2.jpg")  # Save annotated image