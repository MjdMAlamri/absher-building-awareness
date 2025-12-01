import os
import base64
import threading
import time
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional
import numpy as np

import cv2
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from ultralytics import YOLO
import supervision as sv


# ---------- VIDEO SOURCE CONFIG ----------

VIDEO_FILE_NAME = "PeopleWalking.MP4"  # make sure this matches your file name
VIDEO_SOURCE_PATH = Path(__file__).with_name(VIDEO_FILE_NAME)
VIDEO_SOURCE: Any = str(VIDEO_SOURCE_PATH)   # use file
# VIDEO_SOURCE: Any = 0  # uncomment to test with webcam

print(f"[CONFIG] VIDEO_SOURCE set to: {VIDEO_SOURCE}")


# ---------- 1. STATE MODELS ----------

class BuildingStatus(BaseModel):
    total_entries: int
    total_exits: int
    current_inside: int
    last_update_ts: float


class Alert(BaseModel):
    type: str       # "crowding" | "movement"
    level: str      # "info" | "warning" | "critical"
    message: str
    ts: float


class Snapshot(BaseModel):
    image: Optional[str]


class SectionStatus(BaseModel):
    name: str
    current_count: int
    avg_wait_min: float
    peak_occupancy: int


class SectionSummary(BaseModel):
    busiest_section: Optional[str]
    sections: List[SectionStatus]


class SuggestedActions(BaseModel):
    actions: List[str]


# ---------- 2. GLOBAL STATE ----------

state: Dict[str, Any] = {
    "total_entries": 0,
    "total_exits": 0,
    "current_inside": 0,
    "last_update_ts": 0.0,
    "alerts": [],
    "last_image": None,
    "pipeline_running": False,
    "sections": {},
    "section_history": [],
}

CROWD_THRESHOLD = 40
SPIKE_THRESHOLD = 15
SECTION_WAIT_WINDOW_SEC = 5 * 60  # ~5 minutes window


def init_sections(frame_width: int, frame_height: int):
    """
    Define zones:
      - Desk 1, Desk 2, Desk 3 at top
      - Waiting area in middle
      - Entrance (EN) at bottom-right
      - Exit (EX) at bottom-left
    """
    w, h = frame_width, frame_height

    zones: Dict[str, sv.PolygonZone] = {}

    # helper: build a 4-point polygon from an (x1, y1, x2, y2) rectangle
    def rect_to_polygon(x1, y1, x2, y2):
        return np.array([
            [x1, y1],
            [x2, y1],
            [x2, y2],
            [x1, y2],
        ], dtype=np.int32)

    # ---- Desk areas (top row 3 regions) ----
    desk_height = int(h * 0.25)
    desk_width = int(w / 3)

    zones["Desk 1"] = sv.PolygonZone(
        polygon=rect_to_polygon(0, 0, desk_width, desk_height),
        frame_resolution_wh=(w, h),
    )
    zones["Desk 2"] = sv.PolygonZone(
        polygon=rect_to_polygon(desk_width, 0, 2 * desk_width, desk_height),
        frame_resolution_wh=(w, h),
    )
    zones["Desk 3"] = sv.PolygonZone(
        polygon=rect_to_polygon(2 * desk_width, 0, w, desk_height),
        frame_resolution_wh=(w, h),
    )

    # ---- Waiting area (middle band) ----
    waiting_top = int(h * 0.35)
    waiting_bottom = int(h * 0.65)
    zones["Waiting Area"] = sv.PolygonZone(
        polygon=rect_to_polygon(0, waiting_top, w, waiting_bottom),
        frame_resolution_wh=(w, h),
    )

    # ---- Entrance/Exit (bottom band, left/right) ----
    door_top = int(h * 0.7)
    door_bottom = h
    zones["Entrance"] = sv.PolygonZone(
        polygon=rect_to_polygon(int(w * 0.5), door_top, w, door_bottom),
        frame_resolution_wh=(w, h),
    )
    zones["Exit"] = sv.PolygonZone(
        polygon=rect_to_polygon(0, door_top, int(w * 0.5), door_bottom),
        frame_resolution_wh=(w, h),
    )

    # Initialize section stats in state
    sections_state: Dict[str, Dict[str, Any]] = {}
    for name in zones.keys():
        sections_state[name] = {
            "current_count": 0,
            "peak": 0,
            "enter_events": [],  # list of (ts, track_id)
        }

    state["sections"] = sections_state
    return zones


def update_section_stats(zones: Dict[str, sv.PolygonZone],
                         detections: sv.Detections,
                         now: float):
    """
    For each tracked person, see which zone they are in.
    Update per-zone count, peak, and simple waiting-time approximation.
    Uses OpenCV's pointPolygonTest instead of a non-existent PolygonZone.encloses().
    """
    sections_state = state["sections"]

    # Reset counts per frame
    for s in sections_state.values():
        s["current_count"] = 0

    if detections is None or detections.xyxy is None or detections.tracker_id is None:
        return

    # Loop over each tracked box
    for i, box in enumerate(detections.xyxy):
        x1, y1, x2, y2 = box
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)
        tid = int(detections.tracker_id[i])

        point = (cx, cy)

        for section_name, zone in zones.items():
            # zone.polygon is an Nx2 numpy array
            polygon = zone.polygon.astype(np.int32)

            # pointPolygonTest returns:
            #   > 0 if point is inside
            #   = 0 if on edge
            #   < 0 if outside
            if cv2.pointPolygonTest(polygon, point, False) >= 0:
                s = sections_state[section_name]
                s["current_count"] += 1
                if s["current_count"] > s["peak"]:
                    s["peak"] = s["current_count"]
                # add enter event if new track id
                if tid not in [t for _, t in s["enter_events"]]:
                    s["enter_events"].append((now, tid))

    # Trim events older than window and approximate waiting time
    for section_name, s in sections_state.items():
        recent = [(ts, tid) for (ts, tid) in s["enter_events"]
                  if now - ts <= SECTION_WAIT_WINDOW_SEC]
        s["enter_events"] = recent


def build_section_summary(now: float) -> SectionSummary:
    sections_state = state["sections"]
    section_status_list: List[SectionStatus] = []
    busiest = None
    busiest_count = -1

    for name, s in sections_state.items():
        events = s["enter_events"]
        if not events:
            avg_wait = 0.0
        else:
            # crude estimate: if they are still in zone within window,
            # we assume average stay half the window
            avg_wait = SECTION_WAIT_WINDOW_SEC / 120.0  # ~2.5 min

        section_status_list.append(SectionStatus(
            name=name,
            current_count=s["current_count"],
            avg_wait_min=round(avg_wait, 1),
            peak_occupancy=s["peak"]
        ))

        if s["current_count"] > busiest_count:
            busiest_count = s["current_count"]
            busiest = name

    return SectionSummary(
        busiest_section=busiest,
        sections=section_status_list
    )


def build_suggested_actions(section_summary: SectionSummary) -> SuggestedActions:
    actions: List[str] = []

    # Simple rule-based suggestions
    for s in section_summary.sections:
        if s.name.startswith("Desk") and s.current_count >= 5:
            actions.append(
                f"نقترح نقل موظف من قسم آخر لمساندة {s.name} لتقليل وقت الانتظار."
            )

        if s.name == "Waiting Area" and s.current_count >= 8:
            actions.append(
                "منطقة الانتظار مزدحمة، يُفضّل فتح مسار إضافي أو توجيه الزوار للأقسام الأقل ازدحامًا."
            )

        if s.name == "Entrance" and s.current_count >= 5:
            actions.append(
                "يوجد ضغط عند المدخل؛ يُفضّل تخصيص موظف للاستقبال السريع وتنظيم حركة الدخول."
            )

        if s.name == "Exit" and s.current_count >= 5:
            actions.append(
                "حركة الخروج عالية؛ تأكد من انسيابية الممرات وعدم وجود عوائق."
            )

    if not actions:
        actions.append("الوضع مستقر، لا توجد إجراءات عاجلة حاليًا.")

    return SuggestedActions(actions=actions)


# ---------- 3. YOLO + TRACKING PIPELINE ----------

def run_yolo_pipeline():
    global state

    print("[PIPELINE] Initializing YOLO pipeline...")

    # 1) test YOLO model loading
    try:
        print("[PIPELINE] Loading YOLO weights yolov8n.pt ...")
        model = YOLO("yolov8n.pt")  # will download on first run
        print("[PIPELINE] YOLO model loaded OK ✅")
    except Exception as e:
        print("[PIPELINE] Error in YOLO pipeline INIT (model load):", e)
        traceback.print_exc()
        state["pipeline_running"] = False
        return

    # 2) test video source
    print(f"[PIPELINE] Opening video source: {VIDEO_SOURCE}")
    cap = cv2.VideoCapture(VIDEO_SOURCE)

    if not cap.isOpened():
        print("[PIPELINE] ❌ Could not open video source:", VIDEO_SOURCE)
        state["pipeline_running"] = False
        return

    # try reading one frame just to be sure
    test_ok, test_frame = cap.read()
    if not test_ok or test_frame is None:
        print("[PIPELINE] ❌ Could not read first frame from video source")
        cap.release()
        state["pipeline_running"] = False
        return
    else:
        print("[PIPELINE] First frame read OK ✅, starting loop...")

    tracker = sv.ByteTrack()
    line_zone = None
    line_annotator = None
    box_annotator = sv.BoxAnnotator()  # still works, just deprecated in future versions
    zones = None
    zone_annotators = None  # will be dict[str, PolygonZoneAnnotator]

    state["pipeline_running"] = True
    print("[PIPELINE] YOLO pipeline started; reading frames in loop...")

    try:
        frame_idx = 0
        while True:
            ret, frame = cap.read()
            if not ret or frame is None:
                print("[PIPELINE] Stream ended or frame empty, restarting in 2s...")
                time.sleep(2)
                cap.release()
                cap = cv2.VideoCapture(VIDEO_SOURCE)
                continue

            frame_idx += 1
            if frame_idx % 30 == 0:
                print(f"[PIPELINE] Processing frame #{frame_idx}")

            h, w, _ = frame.shape

            if zones is None:
                print(f"[PIPELINE] Initializing zones with frame size {w}x{h}")
                zones = init_sections(w, h)

                # Create a PolygonZoneAnnotator per zone
                zone_annotators = {
                    name: sv.PolygonZoneAnnotator(
                        zone=zone,
                        color=sv.Color.RED,  # Color.red() is deprecated in newer versions
                        thickness=2,
                    )
                    for name, zone in zones.items()
                }

            if line_zone is None:
                start = sv.Point(0, int(h * 0.5))
                end = sv.Point(w, int(h * 0.5))
                line_zone = sv.LineZone(start=start, end=end)
                line_annotator = sv.LineZoneAnnotator(
                    thickness=2, text_scale=0.6, text_thickness=1
                )
                print("[PIPELINE] Line zone initialized")

            # run YOLO
            results = model(frame, imgsz=640, verbose=False)[0]
            detections = sv.Detections.from_ultralytics(results)

            if detections.class_id is not None:
                mask = detections.class_id == 0  # person
                detections = detections[mask]

            tracked = tracker.update_with_detections(detections)

            line_zone.trigger(tracked)

            now = time.time()
            in_count = int(line_zone.in_count)
            out_count = int(line_zone.out_count)

            state["total_entries"] = in_count
            state["total_exits"] = out_count
            state["current_inside"] = in_count - out_count
            state["last_update_ts"] = now

            if frame_idx % 30 == 0:
                print(
                    f"[PIPELINE] Counts -> in={in_count}, "
                    f"out={out_count}, inside={state['current_inside']}"
                )

            # section stats
            update_section_stats(zones, tracked, now)

            # simple alerts
            alerts: List[Dict[str, Any]] = []

            if state["current_inside"] > CROWD_THRESHOLD:
                alerts.append(Alert(
                    type="crowding",
                    level="warning",
                    message=(
                        f"Crowding detected: {state['current_inside']} "
                        f"people inside (limit {CROWD_THRESHOLD})"
                    ),
                    ts=now
                ).dict())

            if in_count > SPIKE_THRESHOLD or out_count > SPIKE_THRESHOLD:
                direction = "entering" if in_count > out_count else "exiting"
                alerts.append(Alert(
                    type="movement_spike",
                    level="info",
                    message=(
                        f"Unusual {direction} activity: "
                        f"in={in_count}, out={out_count}"
                    ),
                    ts=now
                ).dict())

            if alerts:
                state["alerts"] = alerts[-10:]

            # annotate frame
            annotated = frame.copy()
            annotated = box_annotator.annotate(
                scene=annotated,
                detections=tracked
            )
            annotated = line_annotator.annotate(
                frame=annotated,
                line_counter=line_zone
            )

            # draw zones
            if zone_annotators is not None:
                for name, annotator in zone_annotators.items():
                    annotated = annotator.annotate(
                        scene=annotated,
                        label=name
                    )

            ok, buffer = cv2.imencode(".jpg", annotated)
            if ok:
                jpg_as_text = base64.b64encode(buffer).decode("utf-8")
                state["last_image"] = jpg_as_text
            else:
                if frame_idx % 30 == 0:
                    print("[PIPELINE] Warning: cv2.imencode failed")

    except Exception as e:
        print("[PIPELINE] Error in YOLO pipeline loop:", e)
        traceback.print_exc()
    finally:
        state["pipeline_running"] = False
        cap.release()
        print("[PIPELINE] YOLO pipeline stopped")


# start background CCTV thread
threading.Thread(target=run_yolo_pipeline, daemon=True).start()


# ---------- 4. FASTAPI APP & ENDPOINTS ----------

app = FastAPI(title="AI Building Awareness API (YOLO)")


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/processing-status")
def processing_status():
    return {"is_processing": state.get("pipeline_running", False)}


@app.get("/building-status", response_model=BuildingStatus)
def get_building_status():
    return BuildingStatus(
        total_entries=state["total_entries"],
        total_exits=state["total_exits"],
        current_inside=state["current_inside"],
        last_update_ts=state["last_update_ts"],
    )


@app.get("/alerts", response_model=List[Alert])
def get_alerts():
    return [Alert(**a) for a in state["alerts"]]


@app.get("/snapshot", response_model=Snapshot)
def get_snapshot():
    return Snapshot(image=state.get("last_image"))


@app.get("/sections", response_model=SectionSummary)
def get_sections():
    now = time.time()
    return build_section_summary(now)


@app.get("/suggested-actions", response_model=SuggestedActions)
def get_suggested_actions():
    now = time.time()
    summary = build_section_summary(now)
    return build_suggested_actions(summary)


# ---------- 5. DASHBOARD HTML ----------

@app.get("/", response_class=HTMLResponse)
def dashboard():
    return """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8" />
        <title>بوابة الدخول الذكية – لوحة المتابعة</title>
        <style>
            * {
                box-sizing: border-box;
            }
            body {
                margin: 0;
                font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
                             "Tahoma", "Arial", sans-serif;
                background-color: #f5f7fa;
            }

            /* Top green header (Absher style) */
            .top-bar {
                background-color: #00713c;
                color: #ffffff;
                padding: 14px 40px;
                font-size: 16px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .top-bar-left {
                font-weight: 600;
            }
            .top-bar-right {
                font-size: 13px;
                opacity: 0.9;
            }

            /* Center wrapper */
            .page-wrapper {
                padding: 40px 20px 60px;
                display: flex;
                justify-content: center;
            }

            /* Main white card */
            .main-card {
                background-color: #ffffff;
                width: 100%;
                max-width: 1100px;
                border-radius: 18px;
                box-shadow: 0 4px 18px rgba(0, 0, 0, 0.08);
                padding: 26px 28px 22px;
            }

            .title-row {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 10px;
            }

            .title {
                font-size: 22px;
                font-weight: 700;
                color: #1a1f36;
            }

            .subtitle {
                font-size: 13px;
                color: #6f7287;
                margin-bottom: 24px;
            }

            /* Inner layout – right: stats/cards, left: live view */
            .content-layout {
                display: grid;
                grid-template-columns: 2fr 1.5fr;
                gap: 18px;
            }

            /* Generic card in the main card */
            .card {
                background-color: #f9fbfd;
                border-radius: 14px;
                border: 1px solid #e1e4ef;
                padding: 14px 16px;
                margin-bottom: 12px;
            }

            .card h2 {
                margin: 0 0 10px 0;
                font-size: 15px;
                color: #2e384d;
            }

            /* People stats row */
            .stats-row {
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
            }

            .stat-pill {
                flex: 1;
                min-width: 140px;
                background-color: #ffffff;
                border-radius: 999px;
                border: 1px solid #dde3f0;
                padding: 10px 14px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 13px;
                color: #414a63;
            }

            .stat-label {
                display: flex;
                align-items: center;
                gap: 6px;
            }

            .stat-value {
                font-weight: 700;
                color: #00713c;
            }

            /* Alerts */
            .alert {
                background: #ffefef;
                color: #a00000;
                padding: 8px 10px;
                margin: 6px 0;
                border-radius: 10px;
                font-size: 12px;
            }

            .no-alerts {
                color: #0a8f00;
                font-size: 13px;
            }

            /* Sections table */
            table {
                width: 100%;
                border-collapse: collapse;
                font-size: 12px;
            }
            th, td {
                border: 1px solid #dde3f0;
                padding: 5px 6px;
                text-align: center;
            }
            th {
                background: #f0f5ff;
                font-weight: 600;
            }

            .busiest {
                font-size: 13px;
                margin-bottom: 6px;
            }

            /* Actions list */
            ul {
                padding-right: 18px;
                margin: 0;
                font-size: 13px;
                color: #3d445a;
            }

            /* Live view */
            .live-card {
                background-color: #f9fbfd;
                border-radius: 14px;
                border: 1px solid #e1e4ef;
                padding: 14px 16px;
                height: 100%;
                display: flex;
                flex-direction: column;
            }

            .live-card h2 {
                margin: 0 0 10px 0;
                font-size: 15px;
                color: #2e384d;
            }

            .live-img-wrapper {
                flex: 1;
                display: flex;
                align-items: center;
                justify-content: center;
                background-color: #ffffff;
                border-radius: 12px;
                border: 1px solid #dde3f0;
                overflow: hidden;
            }

            img {
                max-width: 100%;
                height: auto;
                display: block;
            }

            /* Info bar under main card */
            .info-bar {
                margin-top: 18px;
                padding: 10px 14px;
                border-radius: 10px;
                background-color: #e7f3ff;
                color: #2770b6;
                font-size: 12px;
                display: flex;
                align-items: center;
                gap: 8px;
            }

            .info-icon {
                width: 18px;
                height: 18px;
                border-radius: 50%;
                border: 1px solid #2770b6;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 11px;
                font-weight: 700;
            }

            @media (max-width: 900px) {
                .content-layout {
                    grid-template-columns: 1fr;
                }
            }

            @media (max-width: 768px) {
                .top-bar {
                    padding: 12px 16px;
                    font-size: 14px;
                }
                .main-card {
                    padding: 20px 18px;
                }
            }
        </style>

        <script>
            async function refresh() {
                const [status, alerts, snap, sections, actions] = await Promise.all([
                    fetch('/building-status').then(r => r.json()),
                    fetch('/alerts').then(r => r.json()),
                    fetch('/snapshot').then(r => r.json()),
                    fetch('/sections').then(r => r.json()),
                    fetch('/suggested-actions').then(r => r.json())
                ]);

                // أرقام الزوار
                document.getElementById('entries').innerText = status.total_entries;
                document.getElementById('exits').innerText = status.total_exits;
                document.getElementById('inside').innerText = status.current_inside;

                // التنبيهات
                let alertDiv = document.getElementById('alerts');
                alertDiv.innerHTML = '';
                if (alerts.length === 0) {
                    alertDiv.innerHTML = '<div class="no-alerts">لا توجد تنبيهات حالياً.</div>';
                } else {
                    alerts.forEach(a => {
                        alertDiv.innerHTML += `
                            <div class="alert">
                                <b>${a.type.toUpperCase()}</b><br/>
                                ${a.message}
                            </div>
                        `;
                    });
                }

                // صورة الكاميرا
                if (snap.image) {
                    let src = snap.image;
                    if (!src.startsWith('data:')) {
                        src = 'data:image/jpeg;base64,' + src;
                    }
                    document.getElementById('liveImage').src = src;
                }

                // جدول الأقسام
                let tbody = document.getElementById('sections-body');
                tbody.innerHTML = '';
                sections.sections.forEach(s => {
                    tbody.innerHTML += `
                        <tr>
                            <td>${s.name}</td>
                            <td>${s.current_count}</td>
                            <td>${s.avg_wait_min}</td>
                            <td>${s.peak_occupancy}</td>
                        </tr>
                    `;
                });

                document.getElementById('busiest').innerText =
                    sections.busiest_section ? sections.busiest_section : '—';

                // التوصيات
                let acts = document.getElementById('actions-list');
                acts.innerHTML = '';
                actions.actions.forEach(a => {
                    acts.innerHTML += `<li>${a}</li>`;
                });
            }

            window.onload = () => {
                refresh();
                setInterval(refresh, 1000);
            };
        </script>
    </head>
    <body>
        <!-- شريط علوي أخضر -->
        <div class="top-bar">
            <div class="top-bar-left">
                بوابة الدخول الذكية
            </div>
            <div class="top-bar-right">
                محاكاة نظام مواعيد الجهات الحكومية
            </div>
        </div>

        <!-- البطاقة الرئيسية -->
        <div class="page-wrapper">
            <div class="main-card">
                <div class="title-row">
                    <div class="title">لوحة متابعة الزوار والكاميرات</div>
                </div>
                <div class="subtitle">
                    عرض فوري لحركة الدخول والخروج، حالة الأقسام، والتنبيهات الذكية المبنية على رؤية الحشود.
                </div>

                <div class="content-layout">
                    <!-- يمين: الإحصائيات / الجداول / التوصيات -->
                    <div>
                        <!-- إحصائيات الزوار -->
                        <div class="card">
                            <h2>👥 إحصائيات الزوار</h2>
                            <div class="stats-row">
                                <div class="stat-pill">
                                    <div class="stat-label">الدخول</div>
                                    <div class="stat-value" id="entries">0</div>
                                </div>
                                <div class="stat-pill">
                                    <div class="stat-label">الخروج</div>
                                    <div class="stat-value" id="exits">0</div>
                                </div>
                                <div class="stat-pill">
                                    <div class="stat-label">المتواجدون الآن</div>
                                    <div class="stat-value" id="inside">0</div>
                                </div>
                            </div>
                        </div>

                        <!-- التنبيهات -->
                        <div class="card">
                            <h2>🚨 التنبيهات الذكية</h2>
                            <div id="alerts">جارِ التحميل...</div>
                        </div>

                        <!-- حالة الأقسام -->
                        <div class="card">
                            <h2>📊 حالة مناطق الخدمة</h2>
                            <div class="busiest">
                                أكثر قسم ازدحاماً الآن:
                                <b id="busiest">—</b>
                            </div>
                            <table>
                                <thead>
                                    <tr>
                                        <th>القسم</th>
                                        <th>العدد الحالي</th>
                                        <th>متوسط الانتظار (دقيقة)</th>
                                        <th>أعلى إشغال مسجّل</th>
                                    </tr>
                                </thead>
                                <tbody id="sections-body"></tbody>
                            </table>
                        </div>

                        <!-- التوصيات -->
                        <div class="card">
                            <h2>🎯 التوصيات المقترحة</h2>
                            <ul id="actions-list">
                                <li>يتم تحديث التوصيات تلقائياً حسب حالة الازدحام.</li>
                            </ul>
                        </div>
                    </div>

                    <!-- يسار: عرض الكاميرا -->
                    <div class="live-card">
                        <h2>🎥 عرض الكاميرا المباشر</h2>
                        <div class="live-img-wrapper">
                            <img id="liveImage" src="" alt="الإطار المعالَج سيظهر هنا" />
                        </div>
                    </div>
                </div>

                <!-- شريط معلومات أسفل البطاقة -->
                <div class="info-bar">
                    <div class="info-icon">i</div>
                    <div>
                        هذه الواجهة تستخدم بيانات وهمية لأغراض التدريب والعرض فقط، ولا ترتبط بأي أنظمة حكومية حقيقية.
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
