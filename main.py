from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from app import predictor
from app.config import settings
from pydantic import BaseModel

app = FastAPI(title="Smart Queue Predictor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class UpdateSettings(BaseModel):
    average_service_time_minutes: int

@app.get("/")
def root():
    return {"status": "ok", "service": "Smart Queue Predictor"}

@app.get("/current-queue")
def current_queue():
    try:
        count = predictor.detect_people()
        return {"people_in_queue": count}
    except Exception as e:
        logger.exception("Error in current_queue")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/waiting-time")
def waiting_time():
    try:
        count = predictor.detect_people()
        wait = predictor.predict_waiting_time(count)
        return {"people_in_queue": count, "estimated_wait_time_minutes": wait}
    except Exception as e:
        logger.exception("Error in waiting_time")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/admin/set-service-time")
def set_service_time(data: UpdateSettings):
    # For demo: update runtime setting. For prod, store in DB or file.
    settings.average_service_time_minutes = data.average_service_time_minutes
    return {"ok": True, "average_service_time_minutes": settings.average_service_time_minutes}
