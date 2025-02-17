import cv2
import torch
from ultralytics import YOLO

# Carrega o modelo YOLO
model = YOLO(r'C:\Users\gustavonc\Documents\2-Programs\6-WSFM_Montagem\trasmisoes_linha_montagem\yolo_detect_v1\pt\modelo_colab_full_dataset_24_10_openvino_model')  # Substitua pelo caminho do seu modelo YOLO treinado

# Função para processar cada quadro e aplicar detecções YOLO
def process_frame(frame):
    # Realiza a detecção com o YOLO
    results = model(frame)

    # Itera sobre as detecções e desenha as bounding boxes no quadro
    for result in results[0].boxes:  # Acessa as detecções com a propriedade 'boxes'
        x1, y1, x2, y2 = result.xyxy[0]  # Coordenadas da bounding box
        confidence = result.conf[0]  # Confiança da detecção
        class_id = result.cls[0]  # ID da classe detectada

        # Desenha a bounding box
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        # Coloca o texto da classe e confiança
        label = f"{model.names[int(class_id)]}: {confidence:.2f}"
        cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    return frame

# Caminho do vídeo de entrada e de saída
video_path = 'posto1.avi'  # Substitua pelo caminho do vídeo de entrada
output_path = 'converted.mp4'  # Caminho para salvar o vídeo processado

# Carrega o vídeo
cap = cv2.VideoCapture(video_path)

# Verifica se o vídeo foi aberto com sucesso
if not cap.isOpened():
    print("Erro ao abrir o vídeo")
    exit()

# Pega as informações do vídeo original
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
fps = cap.get(cv2.CAP_PROP_FPS)

# Define o codec e cria o objeto VideoWriter para salvar o vídeo de saída
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

# Processa o vídeo quadro a quadro
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Processa o quadro com YOLO
    processed_frame = process_frame(frame)
    
    # Escreve o quadro processado no vídeo de saída
    out.write(processed_frame)

    # Exibe o quadro processado (opcional)
    cv2.imshow('YOLO Detection', processed_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera o vídeo e fecha todas as janelas
cap.release()
out.release()
cv2.destroyAllWindows()
