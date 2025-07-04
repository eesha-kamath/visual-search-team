from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
#from typing import List
#from fastapi.responses import JSONResponse
from models.yolov8_model import detect_objects_from_bytes


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
    try:
        contents = await file.read()
        print("Got file:", file.filename)
        objects = detect_objects_from_bytes(contents)
        return {"objects": objects}
    except Exception as e:
        return {"error": str(e)}
