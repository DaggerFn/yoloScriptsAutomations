import cv2
from ultralytics import YOLO

# Carregar o modelo treinado
model = YOLO(r'linha_11m.pt')  # Substitua pelo caminho do modelo treinado

# Caminho do vídeo de entrada
video_path = r'C:\Users\gustavonc\Downloads\videos\3831ac80222e 192.168.0.132_2024-12-13_18-23-18_0.qt'  # Substitua pelo caminho do seu vídeo

# Caminho do vídeo de saída
output_video_path = r'output_video.mp4'  # Substitua pelo caminho desejado para salvar o vídeo

# Abrir o vídeo
cap = cv2.VideoCapture(video_path)

# Obter as dimensões do vídeo
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Verificar se o vídeo foi carregado corretamente
if not cap.isOpened():
    print("Erro ao abrir o vídeo.")
    exit()

# Configurar o VideoWriter para salvar o vídeo processado
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec para o formato MP4
out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

# Loop pelos frames do vídeo
while True:
    ret, frame = cap.read()
    
    if not ret:  # Fim do vídeo
        break

    # Realizar inferência no frame atual
    results = model.predict(frame, augment=True, visualize=False, verbose=False, conf=0.5, iou=0.5)

    # Desenhar as bounding boxes no frame
    annotated_frame = results[0].plot()  # Desenha as caixas no frame

    # Escrever o frame processado no arquivo de saída
    out.write(annotated_frame)

    # Exibir o frame anotado em uma janela OpenCV (opcional)
    cv2.imshow('YOLO Detection', annotated_frame)

    # Pressione 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
out.release()
cv2.destroyAllWindows()

print(f"Vídeo processado salvo em: {output_video_path}")
