# Salva apenas imagens diferentes

import cv2
import os
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import threading
from datetime import datetime
from shutil import copy2

# Variável global
selected_images = []
lock = threading.Lock()

def calculate_histogram(frame):
    histogram = cv2.calcHist([frame], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    cv2.normalize(histogram, histogram)
    return histogram.flatten()

def are_images_similar(hist1, hist2, threshold=0.7):
    similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA)
    return similarity < threshold

def process_rtsp_stream(rtsp_link, output_dir, similarity_threshold, prefix):
    cap = cv2.VideoCapture(rtsp_link)
    if not cap.isOpened():
        print(f"Erro ao acessar a câmera: {rtsp_link}")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print(f"Finalizando captura do link: {rtsp_link}")
            break

        hist = calculate_histogram(frame)

        is_similar = any(are_images_similar(hist, selected_hist, similarity_threshold) for selected_hist in selected_images)

        if not is_similar:
            with lock:
                selected_images.append(hist)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(output_dir, f"{prefix}_{timestamp}.jpg")
            cv2.imwrite(filename, frame)
            print(f"Imagem salva: {filename}")

    cap.release()

def load_selected_images_embeddings(selected_images_dir):
    embeddings = []
    for file in os.listdir(selected_images_dir):
        if file.lower().endswith(('png', 'jpg', 'jpeg')):
            image_path = os.path.join(selected_images_dir, file)
            image = cv2.imread(image_path)
            if image is not None:
                embeddings.append(calculate_histogram(image))
    return embeddings

def main():
    rtsp_links = [
        ("rtsp://admin:fabrica1@192.168.0.131:554/1/1", 'cam_1'),
        ("rtsp://admin:fabrica1@192.168.0.132:554/1/1", 'cam_2'),
        ("rtsp://admin:fabrica1@192.168.0.133:554/1/1", 'cam_3'),
        ("rtsp://admin:fabrica1@192.168.0.134:554/1/1", 'cam_4'),
        ("rtsp://admin:fabrica1@192.168.0.135:554/1/1", 'cam_5'),
        ("rtsp://admin:fabrica1@192.168.0.136:554/1/1", 'cam_6'),
    ]
    
    output_directory = r"/home/sim/code/coleta_imagens/imgs_coletadas"
    selected_images_dir = output_directory

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    global selected_images
    selected_images = load_selected_images_embeddings(selected_images_dir)

    similarity_threshold = 0.2

    with ThreadPoolExecutor() as executor:
        for rtsp_link, prefix in rtsp_links:
            executor.submit(process_rtsp_stream, rtsp_link, output_directory, similarity_threshold, prefix)

if __name__ == "__main__":
    main()
