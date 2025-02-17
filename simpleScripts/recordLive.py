import cv2
import time

# Endereço do stream de vídeo IP
video_url = 'http://10.1.60.155:4000/video_feed'  # Altere para o endereço do seu stream IP

# Nome do arquivo de vídeo de saída
output_filename = 'output_video.avi'

# Definindo o codec e o formato de gravação
fourcc = cv2.VideoWriter_fourcc(*'XVID')
fps = 20.0  # Frames por segundo
frame_size = (640, 480)  # Tamanho do frame (você pode ajustar conforme necessário)

# Abrir conexão com o stream de vídeo
cap = cv2.VideoCapture(video_url)

# Verificar se a conexão foi bem-sucedida
if not cap.isOpened():
    print("Erro ao abrir o stream de vídeo.")
    exit()

# Obtendo a largura e altura reais do vídeo, se for diferente de 640x480
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Criar o objeto VideoWriter para gravar o vídeo
out = cv2.VideoWriter(output_filename, fourcc, fps, (frame_width, frame_height))

# Definir o tempo de gravação (em segundos)
record_time = 680
start_time = time.time()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Erro ao ler o frame.")
        break

    # Exibir o vídeo ao vivo (opcional)
    cv2.imshow('Video Stream', frame)

    # Escrever o frame no arquivo de vídeo
    out.write(frame)

    # Verificar se o tempo de gravação foi atingido
    if time.time() - start_time > record_time:
        print("Tempo de gravação concluído.")
        break

    # Parar se a tecla 'q' for pressionada (opcional)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar os recursos
cap.release()
out.release()
cv2.destroyAllWindows()
