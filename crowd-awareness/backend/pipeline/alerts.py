"""
alert engine with cooldowns, preserving original messages/thresholds
"""
from typing import Any, Dict, List
from pydantic import BaseModel


class Alert(BaseModel):
    type: str
    level: str
    message: str
    ts: float


class AlertEngine:
    def __init__(self, state_store, crowd_threshold: int, spike_threshold: int) -> None:
        self.state = state_store
        self.CROWD_THRESHOLD = crowd_threshold
        self.SPIKE_THRESHOLD = spike_threshold

    def maybe_add_alert(self, alert_key: str, level: str, msg: str, now: float, alerts: List[Dict[str, Any]]) -> None:
        MIN_GAP_SEC = 10
        last_alerts = self.state.last_alert_ts_by_type
        last_ts = last_alerts.get(alert_key, 0)
        if now - last_ts >= MIN_GAP_SEC:
            alerts.append(Alert(type=alert_key, level=level, message=msg, ts=now).dict())
            last_alerts[alert_key] = now

    def build_alerts(self, current_total: int, prev_total: int, now: float) -> None:
        alerts: List[Dict[str, Any]] = []
        delta_inside = abs(current_total - prev_total)

        if current_total > self.CROWD_THRESHOLD:
            self.maybe_add_alert(
                "ازدحام",
                "warning",
                f"تم رصد ازدحام: عدد المتواجدين حالياً {current_total} (الحد المسموح {self.CROWD_THRESHOLD}).",
                now,
                alerts,
            )

        if delta_inside >= self.SPIKE_THRESHOLD:
            if current_total > prev_total:
                self.maybe_add_alert(
                    "زيادة مفاجئة في عدد الوافدين",
                    "info",
                    f"زيادة مفاجئة في عدد الوافدين بمقدار {delta_inside} خلال فترة زمنية قصيرة.",
                    now,
                    alerts,
                )
            else:
                self.maybe_add_alert(
                    "انخفاض مفاجئ في عدد المتواجدين",
                    "info",
                    f"انخفاض مفاجئ في عدد المتواجدين بمقدار {delta_inside} خلال فترة زمنية قصيرة.",
                    now,
                    alerts,
                )

        self.state.add_alerts(alerts, max_keep=3)

