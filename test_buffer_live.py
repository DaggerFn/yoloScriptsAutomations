'''
import cv2
import threading
import time
from collections import deque

# URL RTSP da sua câmera
RTSP_URL = "rtsp://admin:fabrica1@10.1.30.9:554/1/1"

# Buffer de frames (maxlen regula a latência máxima)
buffer = deque(maxlen=100)

def captura():
    cap = cv2.VideoCapture(RTSP_URL)
    if not cap.isOpened():
        print("Não conseguiu abrir a stream RTSP")
        return
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Falha na captura do frame")
            break
        buffer.append(frame)
    cap.release()

def exibicao():
    target_fps = 60.0
    delay = 1.0 / target_fps
    last_frame = None

    while True:
        start = time.time()
        if buffer:
            frame = buffer.popleft()
            last_frame = frame
        elif last_frame is not None:
            # repete o último frame (ou aqui você poderia chamar
            # uma função de interpolação)
            frame = last_frame
        else:
            # ainda não chegou nenhum frame
            continue

        cv2.imshow("RTSP @ 60fps", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # garante ~60 Hz
        elapsed = time.time() - start
        to_wait = delay - elapsed
        if to_wait > 0:
            time.sleep(to_wait)

    cv2.destroyAllWindows()

if __name__ == "__main__":
    t_cap = threading.Thread(target=captura, daemon=True)
    t_disp = threading.Thread(target=exibicao, daemon=True)
    t_cap.start()
    t_disp.start()
    t_cap.join()
    t_disp.join()
'''

import cv2
import time
from collections import deque

def process_rtsp_stream(rtsp_url, target_fps=60.0, buffer_size=100):
    """
    Captura e exibe frames de uma stream RTSP com controle de FPS.

    Args:
        rtsp_url (str): URL da stream RTSP.
        target_fps (float): Taxa de quadros desejada para exibição.
        buffer_size (int): Tamanho máximo do buffer de frames.
    """
    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        print("Não conseguiu abrir a stream RTSP")
        return

    buffer = deque(maxlen=buffer_size)
    delay = 1.0 / target_fps
    last_frame = None

    while True:
        start = time.time()

        # Captura o frame
        ret, frame = cap.read()
        if ret:
            buffer.append(frame)
        else:
            print("Falha na captura do frame")
            if not buffer:
                break

        # Exibe o frame
        if buffer:
            frame = buffer.popleft()
            last_frame = frame
        elif last_frame is not None:
            frame = last_frame
        else:
            continue

        cv2.imshow("RTSP Stream", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Controle de FPS
        elapsed = time.time() - start
        to_wait = delay - elapsed
        if to_wait > 0:
            time.sleep(to_wait)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    RTSP_URL = "rtsp://admin:fabrica1@10.1.30.9:554/1/1"
    process_rtsp_stream(RTSP_URL)