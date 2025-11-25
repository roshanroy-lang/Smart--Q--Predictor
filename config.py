from pydantic import BaseSettings

class Settings(BaseSettings):
    camera_stream: str = "your_camera_stream_or_video.mp4"
    average_service_time_minutes: int = 4
    frame_interval: int = 5
    port: int = 8000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
