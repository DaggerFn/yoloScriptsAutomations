import cv2
from flask import Flask, Response, jsonify
from flask_cors import CORS
import torch
from ultralytics import YOLO
import threading
import time
import os
import sys

app = Flask(__name__)
CORS(app)

# Dicionário de cores para as bounding boxes (uma cor diferente para cada classe)
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

# Dicionário de nomes das classes (substitua pelos nomes das classes do seu modelo)
class_names = {
    0: 'cxEspuma',
    1: 'cxParafusoPreto',
    2: 'cxParafusoPrata',
    3: 'cxVentilador',
    4: 'cxVazia',
}

# Variável para armazenar os resultados das detecções
detection_results = {}
current_detections = {}

# Função para atualizar os resultados das detecções
def update_detection_results():
    global detection_results, current_detections
    while True:
        # Aguarda 30 segundos
        time.sleep(30)
        detection_results = current_detections.copy()

# Função para gerar quadros com detecções
def gen_frames(camera_url, model):
    while True:
        camera = cv2.VideoCapture(camera_url)
        if not camera.isOpened():
            print("Não foi possível abrir a câmera.")
            time.sleep(5)  # Espera um tempo antes de tentar novamente
            continue

        global current_detections

        while True:
            start_time = time.time()

            try:
                success, frame = camera.read()
                if not success:
                    print("Falha na leitura do quadro. Tentando reabrir a câmera.")
                    camera.release()  # Libera o recurso
                    break  # Sai do loop interno para tentar reabrir a câmera

                # Reduzir a resolução do quadro para 1280x720 para reduzir a carga de processamento
                frame = cv2.resize(frame, (1280, 720))

                # Processar a detecção em cada quadro
                results = model(frame)
                frame_detections = {}

                for result in results:
                    for box in result.boxes:
                        x1, y1, x2, y2 = box.xyxy[0].tolist()
                        cls_id = int(box.cls.item())
                        confidence = box.conf.item()
                        color = colors[cls_id % len(colors)]
                        label = class_names.get(cls_id, str(cls_id))

                        if label in frame_detections:
                            frame_detections[label] += 1
                        else:
                            frame_detections[label] = 1

                        # Desenhar a caixa delimitadora e o rótulo no quadro
                        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
                        cv2.putText(frame, f'{label} {confidence:.2f}', (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

                current_detections = frame_detections.copy()

                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

                # Manter o FPS em 10
                elapsed_time = time.time() - start_time
                time.sleep(max(0, 0.1 - elapsed_time))
            except cv2.error as e:
                print(f"Erro no OpenCV: {e}")
                camera.release()
                break

@app.route('/video_feed')
def video_feed():
    camera_url = 'http://10.1.60.137:4000/video_feed'
    model = YOLO('best.pt')

    # Desativar logs do YOLO
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')

    return Response(gen_frames(camera_url, model), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/detections')
def get_detections():
    global detection_results
    return jsonify(detection_results)

if __name__ == '__main__':
    detection_thread = threading.Thread(target=update_detection_results)
    detection_thread.start()

    app.run(host='0.0.0.0', port=4000)
