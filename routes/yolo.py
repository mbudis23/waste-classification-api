from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from models.yolo_model import model_yolo
from config import UPLOAD_DIR
from utils.file_ops import save_upload_file
import os
import uuid

router = APIRouter()

@router.post("/waste-detection/yolo")
async def waste_detection(file: UploadFile = File(...)):
    file_ext = file.filename.split(".")[-1]
    temp_filename = f"{uuid.uuid4()}.{file_ext}"
    temp_file_path = os.path.join(UPLOAD_DIR, temp_filename)

    save_upload_file(file, temp_file_path)
    results = model_yolo(temp_file_path)

    detections = []
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            label = model_yolo.names[class_id]
            confidence = float(box.conf[0])
            detections.append({
                "label": label,
                "confidence": confidence,
                "coordinates": {
                    "x1": int(box.xyxy[0][0]),
                    "y1": int(box.xyxy[0][1]),
                    "x2": int(box.xyxy[0][2]),
                    "y2": int(box.xyxy[0][3]),
                },
            })

    os.remove(temp_file_path)
    return JSONResponse(content={"detections": detections})
