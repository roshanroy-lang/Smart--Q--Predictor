import cv2
from loguru import logger
from app.config import settings

def get_camera():
    cap = cv2.VideoCapture(settings.camera_stream)
    if not cap.isOpened():
        logger.error(f"Failed to open camera stream: {settings.camera_stream}")
        raise Exception("Failed to open camera stream")
    return cap
