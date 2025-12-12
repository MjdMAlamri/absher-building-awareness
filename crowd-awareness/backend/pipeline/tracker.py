"""
byetrack wrapper for person tracking
keeps tracker internal, exposes track(detections) -> tracked detections
"""
import supervision as sv


class PersonTracker:
    def __init__(self) -> None:
        self.tracker = sv.ByteTrack()

    def track(self, detections: sv.Detections) -> sv.Detections:
        return self.tracker.update_with_detections(detections)

