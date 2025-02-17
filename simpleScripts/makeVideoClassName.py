import cv2
import torch
from ultralytics import YOLO

# Mapeamento das classes e seus novos nomes
class_names = {
    0: "Hand_OP",
    1: "Mont_Need_Cover",
    2: "Mont_Finalized",
    3: "Mont_With_Cover",
}

# Cores para cada classe (B, G, R)
colors = {
    "Hand_OP": (255, 0, 0),        # Azul
    "Mont_Need_Cover": (0, 255, 0),# Verde
    "Mont_Finalized": (0, 0, 255), # Vermelho
    "Mont_With_Cover": (0, 255, 255), # Amarelo
}

# Função para renomear e desenhar bounding boxes
def process_frame(frame, results):
    for result in results:
        boxes = result.boxes  # Obtém as bounding boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())  # Coordenadas da bounding box
            class_id = int(box.cls)  # ID da classe
            confidence = box.conf  # Confiança

            if confidence > 0.5:  # Ajuste o limiar conforme necessário
                class_name = class_names.get(class_id, "Desconhecida")

                # Escolhe a cor da classe
                color = colors.get(class_name, (255, 255, 255))  # Branco para classes desconhecidas

                # Desenha a bounding box e o nome da classe
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, class_name, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    return frame

# Função para processar o vídeo completo e salvar o vídeo
def process_video(video_path, model_path, output_path):
    # Carregar o modelo YOLOv8
    model = YOLO(model_path)

    # Captura de vídeo
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Inicializando o VideoWriter para salvar o vídeo
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codificador para salvar em formato MP4
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Processa o frame com o modelo YOLOv8
        results = model(frame)
        frame = process_frame(frame, results)

        # Escreve o frame processado no vídeo de saída
        out.write(frame)

        cv2.imshow("Video", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()  # Libera o arquivo de vídeo
    cv2.destroyAllWindows()

# Exemplo de uso: caminho do vídeo, modelo e caminho de saída
process_video("last.mp4", r"C:\Users\gustavonc\Documents\2- Programs\detec-live-tranmissio-yolo\best.pt", "output_video.mp4")  # Processa e salva o vídeo completo
