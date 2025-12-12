"""
simple state container for pipeline counters, sections, alerts, and snapshot
tracks entries/exits, current_inside, alerts history, section stats, and last image
mutations go through explicit methods to avoid accidental global state drift
"""
from typing import Any, Dict, List, Optional
import time


class StateStore:
    def __init__(self) -> None:
        self.total_entries: int = 0
        self.total_exits: int = 0
        self.current_inside: int = 0
        self.last_update_ts: float = 0.0
        self.alerts: List[Dict[str, Any]] = []
        self.last_image: Optional[str] = None
        self.pipeline_running: bool = False
        self.sections: Dict[str, Dict[str, Any]] = {}
        self.section_history: List[Any] = []
        self.track_last_zone: Dict[int, Optional[str]] = {}
        self.last_total: int = 0
        self.last_alert_ts_by_type: Dict[str, float] = {}

    def mark_running(self, flag: bool) -> None:
        self.pipeline_running = flag

    def set_last_image(self, b64: Optional[str]) -> None:
        self.last_image = b64

    def set_sections(self, sections: Dict[str, Dict[str, Any]]) -> None:
        self.sections = sections
        self.track_last_zone = {}

    def update_counts(self, current_total: int) -> None:
        self.current_inside = current_total
        self.last_total = current_total
        self.last_update_ts = time.time()

    def increment_entry(self) -> None:
        self.total_entries += 1

    def increment_exit(self) -> None:
        self.total_exits += 1

    def add_alerts(self, new_alerts: List[Dict[str, Any]], max_keep: int = 3) -> None:
        if new_alerts:
            self.alerts = (self.alerts + new_alerts)[-max_keep:]

    def sections_snapshot(self) -> Dict[str, Dict[str, Any]]:
        return self.sections

