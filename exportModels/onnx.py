from ultralytics import YOLO

# Load the YOLO11 model
model = YOLO(r"pt\linha_11m.pt")

# Export the model to ONNX format
model.export(format="onnx")  # creates 'yolo11n.onnx'

