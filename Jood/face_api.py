"""
FastAPI wrapper that exposes the existing Python face verification logic
at /verify-face so the Node app can call it.

Run:
  uvicorn face_api:app --host 0.0.0.0 --port 8001

Dependencies (install once):
  pip install fastapi uvicorn
"""

import os
import tempfile
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

# Import your existing verify_face function
try:
    from logic_n_models.FaceRecognition import verify_face
except Exception as e:
    raise ImportError(
        "Cannot import verify_face from logic_n_models.FaceRecognition. "
        "Check PYTHONPATH and that the module exists."
    ) from e

app = FastAPI()


@app.post("/verify-face")
async def verify_face_api(file: UploadFile = File(...)):
    """Accepts a single uploaded image file and runs verify_face()."""
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    try:
        with open(tmp.name, "wb") as f:
            shutil.copyfileobj(file.file, f)

        ok, msg, company_id = verify_face(tmp.name)
        return JSONResponse(
            {"ok": ok, "message": msg, "companyId": company_id},
            status_code=200 if ok else 400,
        )
    except Exception as e:
        return JSONResponse(
            {"ok": False, "message": f"Error: {e}"},
            status_code=500,
        )
    finally:
        try:
            os.remove(tmp.name)
        except Exception:
            pass

