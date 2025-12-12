"""
pipeline controller orchestrates detection, tracking, zoning, movement, alerts, and snapshots
logic remains the same as original monolithic flow; only structured into classes
"""
import time
import traceback
from typing import Any

from .state_store import StateStore
from .video_source import VideoSource
from .detector import YoloPersonDetector
from .tracker import PersonTracker
from .zones import ZoneManager
from .movement import MovementAnalyzer
from .stats import SectionStatistics
from .alerts import AlertEngine
from .annotate import FrameAnnotator


class PipelineController:
    def __init__(self, source: Any) -> None:
        self.state = StateStore()
        self.video = VideoSource(source)
        self.detector = YoloPersonDetector("yolov8n.pt")
        self.tracker = PersonTracker()
        self.zones = ZoneManager()
        self.movement = MovementAnalyzer(self.state, {})
        self.stats = SectionStatistics(self.state)
        self.alerts = AlertEngine(self.state, crowd_threshold=40, spike_threshold=5)
        self.annotator = FrameAnnotator()
        self.thread_started = False

    def start(self) -> None:
        if self.thread_started:
            return
        self.thread_started = True
        import threading
        t = threading.Thread(target=self.run, daemon=True)
        t.start()

    def run(self) -> None:
        self.state.mark_running(True)
        try:
            if not self.video.open():
                self.state.mark_running(False)
                return

            ret, test_frame = self.video.read()
            if not ret or test_frame is None:
                self.state.mark_running(False)
                return

            h, w, _ = test_frame.shape
            zones = self.zones.init_zones(w, h)
            self.state.set_sections({
                name: {"current_count": 0, "peak": 0, "enter_events": []} for name in zones.keys()
            })
            self.movement.reset_for_new_zones(zones)

            while True:
                ok, frame = self.video.read()
                if not ok or frame is None:
                    self.video.restart()
                    continue

                detections = self.detector.detect_people(frame)
                tracked = self.tracker.track(detections)

                now = time.time()
                self.movement.update_section_stats(tracked, now)

                current_total = len(tracked)
                prev_total = self.state.last_total
                self.state.update_counts(current_total)

                self.alerts.build_alerts(current_total, prev_total, now)

                b64 = self.annotator.annotate(frame, tracked, zones)
                if b64:
                    self.state.set_last_image(b64)
        except Exception:
            traceback.print_exc()
        finally:
            self.state.mark_running(False)
            self.video.release()

    def get_building_status(self):
        return {
            "total_entries": self.state.total_entries,
            "total_exits": self.state.total_exits,
            "current_inside": self.state.current_inside,
            "last_update_ts": self.state.last_update_ts,
        }

    def get_alerts(self):
        return self.state.alerts

    def get_snapshot(self):
        return {"image": self.state.last_image}

    def get_sections(self):
        now = time.time()
        summary = self.stats.build_section_summary(now)
        return summary

    def get_suggested_actions(self):
        now = time.time()
        summary = self.stats.build_section_summary(now)
        return self.stats.build_suggested_actions(summary)

    def is_running(self) -> bool:
        return self.state.pipeline_running

