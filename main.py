from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from ultralytics import YOLO
import shutil
import os
import uuid

app = FastAPI()
model = YOLO("models/best.pt")
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)



@app.get("/")
def read_root():
    return {"Status": "Active", "Message": "Welcome to the Waste Detection API"}

@app.post("/waste-detection")
async def waste_detection(file: UploadFile = File(...)):
    file_ext = file.filename.split(".")[-1]
    temp_filename = f"{uuid.uuid4()}.{file_ext}"
    temp_file_path = os.path.join(UPLOAD_DIR, temp_filename)

    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    results = model(temp_file_path)

    detections = []
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            label = model.names[class_id]
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