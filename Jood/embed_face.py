"""
Generate face embedding for a given image path using the same settings
as FaceRecognition.py (GhostFaceNet, opencv backend).

Outputs JSON to stdout:
  { "ok": true, "embedding": [..], "message": "..." }
or on error:
  { "ok": false, "message": "Error ..." }
"""
import sys
import json
import os
import numpy as np
from deepface import DeepFace


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"ok": False, "message": "Image path required"}))
        sys.exit(1)

    image_path = sys.argv[1]
    if not os.path.isfile(image_path):
        print(json.dumps({"ok": False, "message": "Image file not found"}))
        sys.exit(1)

    try:
        embedding = DeepFace.represent(
            img_path=image_path,
            model_name="GhostFaceNet",
            detector_backend="opencv",
            enforce_detection=False,
            align=True
        )[0]["embedding"]

        # Ensure list for JSON serialization
        embedding_list = list(np.array(embedding, dtype=float))
        print(json.dumps({"ok": True, "embedding": embedding_list, "message": "Embedding generated"}))
    except Exception as e:
        print(json.dumps({"ok": False, "message": f"Error generating embedding: {e}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()

