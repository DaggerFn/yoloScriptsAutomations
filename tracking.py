from ultralytics import YOLO
import supervision as sv
from pathlib import Path
import numpy as np
import time
import cv2


# Paramaetro para definir o tipo de objeto a ser rastreado
def sv_init():
    global video_info, byte_tracker, line_zone, line_annotator, box_annotator, cap
    
    cap = cv2.VideoCapture('http://10.1.60.185:4000/video_raw4')
    fps_source = cap.get(cv2.CAP_PROP_FPS)
    width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    video_info = sv.VideoInfo(width=width, height=height, fps=fps_source)
    byte_tracker = sv.ByteTrack(frame_rate=video_info.fps)
    start_pt = sv.Point(x=width - 300, y=0)
    end_pt   = sv.Point(x=width - 300, y=height)
    line_zone = sv.LineZone(start=start_pt, end=end_pt)
    line_annotator = sv.LineZoneAnnotator(thickness=2, text_scale=1.0, text_thickness=2)
    box_annotator  = sv.BoxAnnotator()

#  Recebe frame, video_info, detections e line_zone e retorna o frame com as contagens
def sv_count_obj(frame, video_info: sv.VideoInfo, detections, line_zone: sv.LineZone) -> int:
    detections = sv.Detections.from_ultralytics(detections)

    mask = detections.class_id == frame_class_id
    detections = detections[mask]

    tracked = byte_tracker.update_with_detections(detections)

    line_zone.trigger(tracked)
    in_count = line_zone.in_count
    out_count = line_zone.out_count
    
    labels = [f"id:{tid}" for tid in tracked.tracker_id]
    annotated = box_annotator.annotate(scene=frame.copy(), detections=tracked)
    annotated = line_annotator.annotate(frame=annotated, line_counter=line_zone)
    
    return in_count, out_count, annotated

def init():
    global VIDEO_PATH, MODEL_PATH, CONF_THRESHOLD, model, cap, frame_class_id
    
    VIDEO_PATH = Path("rtsp://admin:fabrica1@10.1.30.9:554/1/1")
    MODEL_PATH = Path(r"C:\Users\gustavonc\Documents\2-Programs\6-WSFM_Montagem\trasmisoes_linha_montagem\yolo-version(old)\YoloFactoryMonitor\yolo11n.pt")
    CONF_THRESHOLD = 0.5

    model = YOLO(str(MODEL_PATH)).to("cpu:0")

    frame_class_id = next(k for k, v in model.names.items() if v.lower() == 'person')
        
    sv_init()

def main():    
    while cap.isOpened():
        start_time = time.time()
        ret, frame = cap.read()
        if not ret:
            break

        result = model.predict(frame, conf=CONF_THRESHOLD, verbose=False)[0]

        count_in, count_out, annotated = sv_count_obj(frame, video_info, result, line_zone)
        
        fps_iter = 1.0 / (time.time() - start_time)
        cv2.putText(annotated, f"FPS: {int(fps_iter)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # cv2.imshow("Annotated", cv2.resize(annotated, (1920, 1080)))
        cv2.imshow("Original", cv2.resize(frame, (1920, 1080)))

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    init()
    main()