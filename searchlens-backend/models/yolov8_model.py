# model/yolo_model.py
from ultralytics import YOLO
from PIL import Image
import io

# Load model once at import
model = YOLO("yolov8n.pt")

def detect_objects_from_bytes(image_bytes: bytes):
    try:
        # Convert bytes to an image
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        # Run detection
        results = model(img)

        detected_objects = set()
        for result in results:
            for box in result.boxes:
                cls_id = int(box.cls[0])
                class_name = model.names[cls_id]
                detected_objects.add(class_name)

        # Return list of unique detected object names
        return list(detected_objects)

    except Exception as e:
        raise Exception(f"Detection failed: {str(e)}")