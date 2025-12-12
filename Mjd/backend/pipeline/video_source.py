from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
VIDEO_PATH = BASE_DIR / "assets" / "videos" / "PeopleWalking2.mp4"

def get_video_capture():
    return cv2.VideoCapture(str(VIDEO_PATH))


# import cv2
# import time
# from typing import Any, Optional


# class VideoSource:
#     """
#     Video source wrapper for file or webcam input.
#
#     This class abstracts OpenCV VideoCapture lifecycle management
#     (open, read, restart, release) so the pipeline controller remains
#     simple and source-agnostic.
#
#     Supports:
#     - Video files (e.g. MP4)
#     - Webcam or camera streams
#     - Safe restart logic for real camera deployments
#     """

#     def __init__(self, source: Any) -> None:
#         self.source = source
#         self.cap: Optional[cv2.VideoCapture] = None

#     def open(self) -> bool:
#         """Open the video source."""
#         if self.cap is not None:
#             self.cap.release()
#         self.cap = cv2.VideoCapture(self.source)
#         return self.cap.isOpened()

#     def read(self):
#         """Read a single frame from the source."""
#         if self.cap is None:
#             return False, None
#         return self.cap.read()

#     def ensure(self) -> bool:
#         """Ensure the video source is open."""
#         if self.cap is None or not self.cap.isOpened():
#             return self.open()
#         return True

#     def restart(self, delay_sec: float = 2.0) -> None:
#         """Restart the video source after a short delay."""
#         if self.cap:
#             self.cap.release()
#         time.sleep(delay_sec)
#         self.open()

#     def release(self) -> None:
#         """Release the video source."""
#         if self.cap:
#             self.cap.release()
#             self.cap = None
