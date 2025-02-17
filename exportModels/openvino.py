from ultralytics import YOLO
# Load a YOLOv8n PyTorch model
model = YOLO(r"pt\linha_11m.pt")

# Export the model
#model.export(format="openvino")  # creates 'yolov8n_openvino_model/'
model.export(format='openvino')#, imgsz=(512))

"""
# Load the exported OpenVINO model

ov_model = YOLO("humanDetectionFineTuned3_openvino_model")

# Run inference
results = ov_model("imagens/img2.jpg")

for result in results:
    #print(result.boxes)  # Print detection boxes
    result.show()  # Display the annotated image
    result.save(filename="result2.jpg")  # Save annotated image
"""