"""
frame annotator: draws boxes, zones, line, and encodes base64 snapshot
"""
from typing import Dict, Any
import cv2
import base64
import supervision as sv


class FrameAnnotator:
    def __init__(self) -> None:
        self.box_annotator = sv.BoxAnnotator()
        self.line_zone = None
        self.line_annotator = None
        self.zone_annotators = None

    def ensure_line(self, h: int, w: int) -> None:
        if self.line_zone is None:
            start = sv.Point(0, int(h * 0.5))
            end = sv.Point(w, int(h * 0.5))
            self.line_zone = sv.LineZone(start=start, end=end)
            self.line_annotator = sv.LineZoneAnnotator(
                thickness=2, text_scale=0.6, text_thickness=1
            )

    def ensure_zones(self, zones: Dict[str, sv.PolygonZone]) -> None:
        if self.zone_annotators is None:
            self.zone_annotators = {
                name: sv.PolygonZoneAnnotator(
                    zone=zone,
                    color=sv.Color.RED,
                    thickness=2,
                    text_thickness=1,
                    text_scale=0.5,
                )
                for name, zone in zones.items()
            }

    def annotate(self, frame, tracked, zones: Dict[str, sv.PolygonZone]):
        h, w, _ = frame.shape
        self.ensure_line(h, w)
        self.ensure_zones(zones)

        if self.line_zone is not None:
            self.line_zone.trigger(tracked)

        annotated = frame.copy()
        annotated = self.box_annotator.annotate(scene=annotated, detections=tracked)

        if self.line_annotator is not None and self.line_zone is not None:
            annotated = self.line_annotator.annotate(frame=annotated, line_counter=self.line_zone)

        if self.zone_annotators is not None:
            for name, annotator in self.zone_annotators.items():
                annotated = annotator.annotate(scene=annotated, label=name)

        ok, buffer = cv2.imencode(".jpg", annotated)
        if not ok:
            return None
        return base64.b64encode(buffer).decode("utf-8")

