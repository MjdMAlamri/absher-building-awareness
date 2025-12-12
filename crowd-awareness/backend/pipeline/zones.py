"""
zone management: defines polygons and assigns sections
keeps same geometry/behavior as original code
"""
from typing import Any, Dict, Optional
import numpy as np
import supervision as sv


class ZoneManager:
    def __init__(self) -> None:
        self.zones: Dict[str, sv.PolygonZone] = {}

    def init_zones(self, frame_width: int, frame_height: int) -> Dict[str, sv.PolygonZone]:
        w, h = frame_width, frame_height
        zones: Dict[str, sv.PolygonZone] = {}

        def rect_to_polygon(x1, y1, x2, y2):
            return np.array([
                [x1, y1],
                [x2, y1],
                [x2, y2],
                [x1, y2],
            ], dtype=np.int32)

        desk_height = int(h * 0.25)
        desk_width = int(w / 3)
        zones["Desk 1"] = sv.PolygonZone(polygon=rect_to_polygon(0, 0, desk_width, desk_height))
        zones["Desk 2"] = sv.PolygonZone(polygon=rect_to_polygon(desk_width, 0, 2 * desk_width, desk_height))
        zones["Desk 3"] = sv.PolygonZone(polygon=rect_to_polygon(2 * desk_width, 0, w, desk_height))

        waiting_top = int(h * 0.35)
        waiting_bottom = int(h * 0.65)
        zones["Waiting Area"] = sv.PolygonZone(polygon=rect_to_polygon(0, waiting_top, w, waiting_bottom))

        door_top = int(h * 0.7)
        door_bottom = h
        zones["Entrance"] = sv.PolygonZone(polygon=rect_to_polygon(int(w * 0.5), door_top, w, door_bottom))
        zones["Exit"] = sv.PolygonZone(polygon=rect_to_polygon(0, door_top, int(w * 0.5), door_bottom))

        self.zones = zones
        return zones

    def point_zone(self, point, zones: Dict[str, sv.PolygonZone]) -> Optional[str]:
        for section_name, zone in zones.items():
            polygon = zone.polygon.astype(np.int32)
            if sv.geometry.point_in_polygon(point, polygon):
                return section_name
        return None

