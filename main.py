from fastapi import FastAPI
# from routes import yolo, efficientnet
from routes import efficientnet

app = FastAPI()
# app.include_router(yolo.router)
app.include_router(efficientnet.router)

@app.get("/")
def read_root():
    return {"Status": "Active", "Message": "Welcome to the Waste Detection API"}