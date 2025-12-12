"""
Standalone script to verify face from command line.
Called directly from Node.js server.
"""
import sys
import json
from logic_n_models.FaceRecognition import verify_face

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"ok": False, "message": "Image path required"}))
        sys.exit(1)
    
    image_path = sys.argv[1]
    national_id = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        ok, msg, user_id = verify_face(image_path, national_id=national_id)
        result = {
            "ok": ok,
            "message": msg,
            "userId": user_id
        }
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({
            "ok": False,
            "message": f"Error: {str(e)}"
        }))
        sys.exit(1)

