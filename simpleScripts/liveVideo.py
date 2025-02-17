import cv2
from flask import Flask, Response

app = Flask(__name__)

# Configurações da câmera IP
camera_url = "http://10.1.60.155:4000/video_feed"

def generate_frames():
    cap = cv2.VideoCapture(camera_url)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # Reduz a resolução para melhorar o desempenho
            frame = cv2.resize(frame, (1920, 1080))
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
