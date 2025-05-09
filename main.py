from fastapi import FastAPI
from routes import yolo, efficientnet

app = FastAPI()
app.include_router(yolo.router)
app.include_router(efficientnet.router)

@app.get("/")
def read_root():
    return {"Status": "Active", "Message": "Welcome to the Waste Detection API"}

# from fastapi import FastAPI, UploadFile, File
# from fastapi.responses import JSONResponse
# # from ultralytics import YOLO
# import shutil
# import os
# import uuid
# from PIL import Image
# import torch
# import torchvision.transforms as transforms
# from efficientnet_pytorch import EfficientNet
# import torch.nn as nn

# app = FastAPI()
# model_yolo = YOLO("models/best.pt")



# num_classes = 44
# class_names = [
#     "Aerosols",
# "Aluminum can",
# "Aluminum caps",
# "Cardboard",
# "Cellulose",
# "Ceramic",
# "Combined plastic",
# "Container for household chemicals",
# "Disposable tableware",
# "Electronics",
# "Foil",
# "Furniture",
# "Glass bottle",
# "Iron utensils",
# "Liquid",
# "Metal shavings",
# "Milk bottle",
# "Organic",
# "Paper bag",
# "Paper cups",
# "Paper shavings",
# "Paper",
# "Papier mache",
# "Plastic bag",
# "Plastic bottle",
# "Plastic can",
# "Plastic canister",
# "Plastic caps",
# "Plastic cup",
# "Plastic shaker",
# "Plastic shavings",
# "Plastic toys",
# "Postal packaging",
# "Printing industry",
# "Scrap metal",
# "Stretch film",
# "Tetra pack",
# "Textile",
# "Tin",
# "Unknown plastic",
# "Wood",
# "Zip plastic bag", 
# "Ramen Cup",
# "Food Packet"
# ]

# model_eff = EfficientNet.from_pretrained('efficientnet-b0')
# model_eff = EfficientNet.from_name('efficientnet-b0')
# model_eff._fc = nn.Linear(model_eff._fc.in_features, num_classes)
# model_eff.load_state_dict(torch.load("models/efficientnet_garbage_classifier.pth", map_location="cpu"))
# model_eff.eval()

# val_transform = transforms.Compose([
#     transforms.Resize((300, 300)),
#     transforms.ToTensor(),
# ])

# UPLOAD_DIR = "uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# def map_to_six_classes(predicted_class):
#     if predicted_class in ["Organic"]:
#         return "organik"
#     elif predicted_class in ["Paper", "Paper bag", "Paper cups", "Paper shavings", "Papier mache", "Cardboard", "Cellulose", "Printing industry"]:
#         return "kertas"
#     elif predicted_class in [
#         "Plastic bag", "Plastic bottle", "Plastic can", "Plastic canister", "Plastic caps", "Plastic cup", "Plastic shaker",
#         "Plastic shavings", "Plastic toys", "Combined plastic", "Zip plastic bag", "Stretch film", "Tetra pack", "Unknown plastic", "Ramen Cup", "Food Packet"
#     ]:
#         return "plastik"
#     elif predicted_class in ["Glass bottle", "Ceramic"]:
#         return "kaca"
#     elif predicted_class in [
#         "Aluminum can", "Aluminum caps", "Iron utensils", "Metal shavings", "Scrap metal", "Tin", "Foil"
#     ]:
#         return "logam"
#     else:
#         return "lainnya"




# @app.get("/")
# def read_root():
#     return {"Status": "Active", "Message": "Welcome to the Waste Detection API"}

# @app.post("/waste-detection/yolo")
# async def waste_detection(file: UploadFile = File(...)):
#     file_ext = file.filename.split(".")[-1]
#     temp_filename = f"{uuid.uuid4()}.{file_ext}"
#     temp_file_path = os.path.join(UPLOAD_DIR, temp_filename)

#     with open(temp_file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     results = model_yolo(temp_file_path)

#     detections = []
#     for result in results:
#         for box in result.boxes:
#             class_id = int(box.cls[0])
#             label = model_yolo.names[class_id]
#             confidence = float(box.conf[0])
#             detections.append({
#                 "label": label,
#                 "confidence": confidence,
#                 "coordinates": {
#                     "x1": int(box.xyxy[0][0]),
#                     "y1": int(box.xyxy[0][1]),
#                     "x2": int(box.xyxy[0][2]),
#                     "y2": int(box.xyxy[0][3]),
#                 },
#             })

#     os.remove(temp_file_path)
#     return JSONResponse(content={"detections": detections})

# @app.post("/waste-classification/efficientnet")
# async def classify_waste(file: UploadFile = File(...)):
#     file_ext = file.filename.split(".")[-1]
#     temp_filename = f"{uuid.uuid4()}.{file_ext}"
#     temp_file_path = os.path.join(UPLOAD_DIR, temp_filename)

#     with open(temp_file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     image = Image.open(temp_file_path).convert("RGB")
#     input_tensor = val_transform(image).unsqueeze(0)

#     with torch.no_grad():
#         outputs = model_eff(input_tensor)
#         _, predicted = torch.max(outputs, 1)
#         predicted_label = class_names[predicted.item()]
#         confidence = torch.softmax(outputs, dim=1)[0][predicted.item()].item()
#         predicted_label = map_to_six_classes(predicted_label)

#     os.remove(temp_file_path)
#     return JSONResponse(content={
#         "prediction": predicted_label,
#         "confidence": round(confidence, 4)
#     })