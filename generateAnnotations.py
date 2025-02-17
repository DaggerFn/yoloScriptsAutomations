import os
import cv2
import torch
from ultralytics import YOLO

# Carregar o modelo YOLO pré-treinado
model = YOLO(r'modelo_linha_final.pt')  # Substitua pelo caminho do seu modelo treinado

# Pasta onde estão suas imagens não anotadas
image_folder = r'C:\Users\gustavonc\Desktop\test\picture'

# Pasta para salvar as anotações geradas automaticamente
output_folder = r'C:\Users\gustavonc\Desktop\test\label'
if not os.path.exists(output_folder):    os.makedirs(output_folder)

# Função para salvar as anotações em formato YOLO
def save_yolo_format(output_path, img_shape, boxes, class_ids):
    img_height, img_width = img_shape
    with open(output_path, 'w') as f:
        for box, class_id in zip(boxes, class_ids):
            x_center = (box[0] + box[2]) / 2.0 / img_width
            y_center = (box[1] + box[3]) / 2.0 / img_height
            width = (box[2] - box[0]) / img_width
            height = (box[3] - box[1]) / img_height
            if class_id == 1.0:
                class_id = int(1)
                f.write(f"{class_id} {x_center} {y_center} {width} {height}\n")
            if class_id == 0.0:
                class_id = int(0)
                f.write(f"{class_id} {x_center} {y_center} {width} {height}\n")
            if class_id == 2.0:
                class_id = int(2)
                f.write(f"{class_id} {x_center} {y_center} {width} {height}\n")

            
# Loop para processar todas as imagens da pasta
for img_name in os.listdir(image_folder):
    if img_name.endswith(('.jpg', '.png', '.jpeg')):
        img_path = os.path.join(image_folder, img_name)
        img = cv2.imread(img_path)

        # Fazer inferência com o modelo pré-treinado
        results = model(img)

        # Para cada imagem, obter as predições
        for result in results:
            boxes = result.boxes.xyxy.cpu().numpy()  # Coordenadas das bounding boxes [x_min, y_min, x_max, y_max]
            class_ids = result.boxes.cls.cpu().numpy()  # IDs das classes preditas
            confidences = result.boxes.conf.cpu().numpy()  # Confiança das detecções

            # Filtrar predições com baixa confiança (opcional)
            min_confidence = 0.5
            boxes = boxes[confidences >= min_confidence]
            class_ids = class_ids[confidences >= min_confidence]

            # Nome do arquivo de saída para anotações
            output_path = os.path.join(output_folder, img_name.replace('.jpg', '.txt').replace('.png', '.txt'))

            # Salvar em formato YOLO
            save_yolo_format(output_path, img.shape[:2], boxes, class_ids)

        print(f"Anotações geradas para a imagem {img_name}")
