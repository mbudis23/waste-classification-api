from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from PIL import Image
import numpy as np
import io

from models.bin_yolo_model import detect_and_classify_bin

router = APIRouter()

@router.post("/detect-bin")
async def detect_trash_bin(file: UploadFile = File(...)):
    contents = await file.read()
    img = Image.open(io.BytesIO(contents)).convert("RGB")
    np_img = np.array(img)

    results = detect_and_classify_bin(np_img)
    return JSONResponse(content={"detections": results})
