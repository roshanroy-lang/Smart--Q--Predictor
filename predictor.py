from ultralytics import YOLO
import time
from app.camera import get_camera
from app.config import settings
from loguru import logger

# Lazy-load model and camera to avoid heavy imports during startup
_model = None
_cap = None
_last_count = 0
_last_time = 0

def _ensure_resources():
    global _model, _cap
    if _model is None:
        logger.info("Loading YOLO model yolov8n.pt (may download first time)...")
        _model = YOLO("yolov8n.pt")
    if _cap is None:
        _cap = get_camera()
    return _model, _cap

def detect_people():
    global _last_count, _last_time
    model, cap = _ensure_resources()
    current_time = time.time()
    if current_time - _last_time < settings.frame_interval:
        return _last_count
    ret, frame = cap.read()
    if not ret:
        logger.warning("Failed to read frame from camera")
        return _last_count
    results = model(frame, verbose=False)
    count = 0
    for r in results:
        for box in r.boxes:
            if int(box.cls) == 0:
                count += 1
    _last_count = count
    _last_time = current_time
    logger.debug(f"Detected {count} people")
    return count

def predict_waiting_time(people_count):
    return people_count * settings.average_service_time_minutes
