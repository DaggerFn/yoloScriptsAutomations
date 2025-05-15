import supervision as sv



def image_updater():

    frames = []
    pass

def init_sv():
    global frames
    cap = cv2.VideoCapture('rtsp://admin:admin@10.1.30.9:554/1/1')
    fps_source = cap.get(cv2.CAP_PROP_FPS)
    width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    video_info = sv.VideoInfo(width=width, height=height, fps=fps_source)
    byte_tracker = sv.ByteTrack(frame_rate=video_info.fps)
    start_pt = sv.Point(x=width - 300, y=0)
    end_pt   = sv.Point(x=width - 300, y=height)
    line_zone = sv.LineZone(start=start_pt, end=end_pt)
    line_annotator = sv.LineZoneAnnotator(thickness=2, text_scale=1.0, text_thickness=2)
    box_annotator  = sv.BoxAnnotator()

    pass 

def sv_count_obj():
    
    # Extract the detections from the ultralytics format
    detections = sv.Detections.from_ultralytics(detections)

    # Filter the detections based on the class ID
    mask = detections.class_id == frame_class_id
    detections = detections[mask]

    # Update the byte tracker with the filtered detections
    tracked = byte_tracker.update_with_detections(detections)

    # Trigger the line zone to count the objects
    line_zone.trigger(tracked)
    in_count = line_zone.in_count
    out_count = line_zone.out_count
    
    # Generate labels for the tracked objects
    labels = [f"id:{tid}" for tid in tracked.tracker_id]
    
    # Annotate the scene with bounding boxes
    annotated = box_annotator.annotate(scene=frame.copy(), detections=tracked)
    
    # Annotate the scene with the line counter
    annotated = line_annotator.annotate(frame=annotated, line_counter=line_zone)
    
    return in_count, out_count, annotated

'''
A função sv_count basciamente faz o seguinte:
Recebe o resultado das deteçoes no frame feita pelo YOLO, logo se intera do objeto
a ser identificado, logo a detecçao e atualiza em sua lista (byte_tracker)


'''