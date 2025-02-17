from ultralytics.utils.benchmarks import benchmark
from ultralytics import YOLO

# Benchmark on GPU
#model = YOLO(r'C:\Users\gustavonc\Documents\2-Programs\6-WSFM_Montagem\trasmisoes_linha_montagem\yolo_detect_v1\modelo_colab_full_dataset_09_10.pt')

benchmark(model="yolo11n.pt", data="coco8.yaml", imgsz=640, half=False, device=0)