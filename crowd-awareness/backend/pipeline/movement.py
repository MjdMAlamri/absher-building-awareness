"""
movement analyzer: entrance/exit logic and section counting
preserves original behavior and thresholds
"""
from typing import Any, Dict, Optional
import supervision as sv


class MovementAnalyzer:
    def __init__(self, state_store, zones: Dict[str, Any]) -> None:
        self.state = state_store
        self.zones = zones

    def reset_for_new_zones(self, zones: Dict[str, Any]) -> None:
        self.zones = zones
        self.state.track_last_zone = {}

    def update_section_stats(self, detections: sv.Detections, now: float) -> None:
        sections_state = self.state.sections
        track_last_zone = self.state.track_last_zone

        for s in sections_state.values():
            s["current_count"] = 0

        if detections is None or detections.xyxy is None or detections.tracker_id is None:
            return

        for i, box in enumerate(detections.xyxy):
            x1, y1, x2, y2 = box
            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)
            tid = int(detections.tracker_id[i])
            point = (cx, cy)

            current_zone: Optional[str] = None
            for section_name, zone in self.zones.items():
                polygon = zone.polygon.astype(np.int32)
                if sv.geometry.point_in_polygon(point, polygon):
                    current_zone = section_name
                    s = sections_state[section_name]
                    s["current_count"] += 1
                    if s["current_count"] > s.get("peak", 0):
                        s["peak"] = s["current_count"]
                    if tid not in [t for _, t in s.get("enter_events", [])]:
                        s["enter_events"].append((now, tid))

            prev_zone = track_last_zone.get(tid)
            if prev_zone != current_zone:
                if current_zone == "Entrance":
                    self.state.increment_entry()
                if current_zone == "Exit":
                    self.state.increment_exit()

            track_last_zone[tid] = current_zone

        SECTION_WAIT_WINDOW_SEC = 5 * 60
        for section_name, s in sections_state.items():
            recent = [(ts, tid) for (ts, tid) in s["enter_events"] if now - ts <= SECTION_WAIT_WINDOW_SEC]
            s["enter_events"] = recent

