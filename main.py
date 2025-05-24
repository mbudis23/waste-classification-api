from fastapi import FastAPI
# from routes import yolo, efficientnet
from routes import efficientnet
# from routes import recycle_bin
from routes import bin_detection

app = FastAPI()
# app.include_router(yolo.router)
app.include_router(efficientnet.router)
# app.include_router(recycle_bin.router)
app.include_router(bin_detection.router)

@app.get("/")
def read_root():
    return {"Status": "Active", "Message": "Welcome to the Waste Detection API"}