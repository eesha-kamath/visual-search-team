from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from models.yolov8_model import detect_objects
from typing import List
from fastapi.responses import JSONResponse

app = FastAPI()

# Allow frontend (adjust port as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or your frontend port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/detect-objects")
async def detect_objects(file: UploadFile = File(...)):
    # Simulate detection
    detected = ["curtain", "shelf", "lamp"]  # 🔁 Replace with real model logic later

    return JSONResponse(content={"objects": detected})