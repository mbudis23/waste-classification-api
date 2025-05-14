from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from PIL import Image
import torch
from torchvision import transforms
import uuid, os

from models.efficientnet_model import model_eff, class_names
from config import UPLOAD_DIR
from utils.class_mapper import map_to_three_classes
from utils.file_ops import save_upload_file

router = APIRouter()

val_transform = transforms.Compose([
    transforms.Resize((300, 300)),
    transforms.ToTensor(),
])

@router.post("/waste-classification/efficientnet")
async def classify_waste(file: UploadFile = File(...)):
    file_ext = file.filename.split(".")[-1]
    temp_filename = f"{uuid.uuid4()}.{file_ext}"
    temp_file_path = os.path.join(UPLOAD_DIR, temp_filename)

    save_upload_file(file, temp_file_path)
    image = Image.open(temp_file_path).convert("RGB")
    input_tensor = val_transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model_eff(input_tensor)
        _, predicted = torch.max(outputs, 1)
        predicted_label = class_names[predicted.item()]
        confidence = torch.softmax(outputs, dim=1)[0][predicted.item()].item()
        predicted_label = map_to_three_classes(predicted_label)

    os.remove(temp_file_path)

    return JSONResponse(content={
        "prediction": predicted_label,
        "confidence": round(confidence, 4)
    })
