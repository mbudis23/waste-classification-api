from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from models.recycle_bin_model import model, labels
from utils.image_preprocessing import preprocess_image

router = APIRouter()

def classify_waste_type(color_label: str) -> str:
    color_label = color_label.lower()
    if "green" in color_label:
        return "Organik"
    elif "orange" in color_label or "yellow" in color_label:
        return "Anorganik"
    elif "red" in color_label:
        return "B3"
    else:
        return "Tidak Diketahui"

@router.post("/recycle_bin_classify")
async def classify_recycle_bin(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
        raise HTTPException(status_code=400, detail="File must be an image (jpg, jpeg, png)")
    
    try:
        image_bytes = await file.read()
        features = preprocess_image(image_bytes)
        prediction_index = model.predict(features)[0]
        predicted_label = labels[prediction_index]
        waste_category = classify_waste_type(predicted_label)
        
        return JSONResponse(content={
            "predicted_color": predicted_label,
            "waste_category": waste_category
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
