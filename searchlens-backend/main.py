from fastapi import FastAPI, File, UploadFile, Body
from fastapi.middleware.cors import CORSMiddleware
from model.clip_model import run_clip_on_image
from model.url_generator import build_walmart_url

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/detect-attributes")
async def detect_attributes(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        result = run_clip_on_image(image_bytes)
        return result
    except Exception as e:
        return {"error": str(e)}

@app.post("/generate-url")
def generate_url(category: str = Body(...), attributes: list[str] = Body(...)):
    try:
        url = build_walmart_url(category, attributes)
        return {"url": url}
    except Exception as e:
        return {"error": str(e)}
