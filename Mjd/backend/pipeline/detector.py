"""
person detector wrapper around ultralytics yolo
loads the model once and exposes detect_people(frame) returning supervision.Detections filtered to class person
"""
import supervision as sv
from ultralytics import YOLO


class YoloPersonDetector:
    def __init__(self, model_name: str = "yolov8n.pt") -> None:
        self.model = YOLO(model_name)

    def detect_people(self, frame) -> sv.Detections:
        results = self.model(frame, imgsz=640, verbose=False)[0]
        detections = sv.Detections.from_ultralytics(results)
        if detections.class_id is not None:
            mask = detections.class_id == 0
            detections = detections[mask]
        return detections

