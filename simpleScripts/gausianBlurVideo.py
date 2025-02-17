import cv2
from ultralytics import YOLO

# Carregar o modelo YOLOv8n-Pose
model = YOLO("models/yolov8n-pose.pt")

# URL da transmissão de vídeo
video_url = "http://10.1.60.155:4000/video_feed"

# Abrir a transmissão de vídeo
cap = cv2.VideoCapture(video_url)

while cap.isOpened():
    ret, frame = cap.read()
    
    if not ret:
        print("Falha ao capturar o frame da transmissão de vídeo.")
        break
    
    # Realizar a detecção usando o modelo YOLO
    results = model(frame)

    # Iterar sobre cada detecção
    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            
            # Extrair a região da bounding box
            roi = frame[y1:y2, x1:x2]
            
            # Aplicar blur na região da bounding box
            blur = cv2.GaussianBlur(roi, (51, 51), 30)
            
            # Substituir a região original pela borrada
            frame[y1:y2, x1:x2] = blur

    # Exibir o frame com as áreas borradas
    cv2.imshow("Detecção com Blur", frame)

    # Pressione 'q' para sair do loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar a captura de vídeo e fechar as janelas
cap.release()
cv2.destroyAllWindows()
