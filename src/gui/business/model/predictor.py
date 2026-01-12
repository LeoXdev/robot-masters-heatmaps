def predict(model, frame):
    """
    predict takes a yolo model and a cv2 frame to make a prediction with the model over the frame.
    Returns a list containing detections where an even number indicates the class name and the following
    odd number holds the bounding box in x1, y1, x2, y2 format.
    """
    res = model(frame, imgsz=800, conf=0.85, verbose=False)[0]
    detections = []
    
    for box in res.boxes:
        class_id = int(box.cls[0])
        class_name = res.names[class_id]


        x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())

        detections.append((class_name, [x1, y1, x2, y2]))

    return detections
