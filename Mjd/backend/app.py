"""
py app entrypoint for yolo+byetrack pipeline
json-only api, frontend is decoupled (netlify)
"""
import torch
from pathlib import Path
from typing import Any
from fastapi import FastAPI
from pydantic import BaseModel

from pipeline.controller import PipelineController
from pipeline.stats import SectionSummary, SuggestedActions

# ---- PyTorch 2.6 compatibility: force weights_only=False in torch.load ----
_real_torch_load = torch.load


def torch_load_allow_code(*args, **kwargs):
    kwargs.setdefault("weights_only", False)
    return _real_torch_load(*args, **kwargs)


torch.load = torch_load_allow_code
# ---------------------------------------------------------------------------

VIDEO_FILE_NAME = "PeopleWalking2.MP4"
VIDEO_SOURCE_PATH = Path(__file__).with_name(VIDEO_FILE_NAME)
VIDEO_SOURCE: Any = str(VIDEO_SOURCE_PATH)
# VIDEO_SOURCE: Any = 0  # webcam if needed

app = FastAPI(title="AI Building Awareness API (YOLO)")


class BuildingStatus(BaseModel):
    total_entries: int
    total_exits: int
    current_inside: int
    last_update_ts: float


class AlertModel(BaseModel):
    type: str
    level: str
    message: str
    ts: float


class Snapshot(BaseModel):
    image: Any


controller = PipelineController(VIDEO_SOURCE)
controller.start()


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/processing-status")
def processing_status():
    return {"is_processing": controller.is_running()}


@app.get("/building-status", response_model=BuildingStatus)
def get_building_status():
    data = controller.get_building_status()
    return BuildingStatus(**data)


@app.get("/alerts", response_model=list[AlertModel])
def get_alerts():
    return [AlertModel(**a) for a in controller.get_alerts()]


@app.get("/snapshot", response_model=Snapshot)
def get_snapshot():
    return Snapshot(**controller.get_snapshot())


@app.get("/sections", response_model=SectionSummary)
def get_sections():
    return controller.get_sections()


@app.get("/suggested-actions", response_model=SuggestedActions)
def get_suggested_actions():
    return controller.get_suggested_actions()

